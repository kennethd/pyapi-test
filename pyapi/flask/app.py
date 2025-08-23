"""
This module provides a base Flask server, not yet configured for a specific API

In non-monorepo situations this module might be distributed org-wide to provide
a consistent implementation of all Flask-based services, which would be
implemented in dependent repos.

For this project, the separation is only at the module-level.  `pyapi.flask.api`
uses the app factory & helpers defined here to create an API server, which is
then configured with implementation found in `pyapi.flask.blueprints`
"""
import argparse
import logging
import os
from pathlib import Path
import tempfile

from flask import Flask, jsonify, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.middleware.profiler import ProfilerMiddleware

log = logging.getLogger(__name__)


# default is '/home/kenneth/git/pyapi-test/static'
# for distro with package, 'static' must be in 'pyapi' subdirectory
PROJECT_DIR = Path(__file__).parent.parent.parent.absolute()
STATIC_DIR = os.path.sep.join([str(PROJECT_DIR), 'pyapi', 'static'])

# FLASKAPP_ARGPARSE_DEFAULTS can be useful when testing custom FlaskAppArgParser implementations:
#   args = StrikeReportsArgParser.parse_args(['--port', '9999'])
#   expect = argparse.Namespace(port=9999, **FLASKAPP_ARGPARSE_DEFAULTS)
#   self.assertEqual(args, expect)
FLASKAPP_ARGPARSE_DEFAULTS = {
    'config': None,
    'debug': False,
    'https': False,
    'ssl_key': '',
    'ssl_crt': '',
    'profiler': False,
    'profiler_datadir': '',
    'proxy_fix': False,
}


FlaskAppArgParser = argparse.ArgumentParser(description="Arg parser for Flask app factory")
FlaskAppArgParser.add_argument("--config", type=str,
                               help="string path to config module: myapp.config")
# port is used by app init script as arg to app.run()
FlaskAppArgParser.add_argument("--port", type=int, required=True, help="port")
FlaskAppArgParser.add_argument("--debug", action="store_true", default=False,
                               help="put app into debug mode")
# app should be behind https terminus, in case debugging https stuff:
# (these args are only used by app init script as args to app.run())
FlaskAppArgParser.add_argument("--https", action="store_true", default=False,
                               help="listen via https")
FlaskAppArgParser.add_argument("--ssl-key", default="")
FlaskAppArgParser.add_argument("--ssl-crt", default="")
# options to enable Flask extensions
FlaskAppArgParser.add_argument("--profiler", action="store_true", default=False,
                               help="enable Werkzeug profiler")
FlaskAppArgParser.add_argument("--profiler-datadir", type=str, default="",
                               help="path to write pstat data to")
FlaskAppArgParser.add_argument("--proxy-fix", action="store_true", default=False,
                               help="add X-Forwarded-For headers")


def configured_app(import_name, debug=False, config_module=None,
                   profiler=False, profiler_datadir="",
                   proxy_fix=False, sqlalchemy=False):
    """instantiate a Flask app

    for details see https://flask.palletsprojects.com/en/2.0.x/api/#flask.Flask

     * import_name: the name of your app package
     * debug: put flask app into debug mode
     * config_module: python module path to load config from
     * profiler: bool. activate flask.contrib.profiler.ProfilerMiddleware
     * profiler_datadir: str. path for pstat output
     * proxy_fix: bool. activate werkzeug.contrib.fixers.ProxyFix
     * sqlalchemy: bool. sets a couple SQLALCHEMY_ config vars

    Environment variables supported:

    FLASKAPP_CONFIG envvar module, values will override those in config_module
    """
    flask_kwargs = {
        'static_folder': STATIC_DIR,
    }

    app = Flask(import_name, **flask_kwargs)
    app.secret_key = os.urandom(24)

    if sqlalchemy:
        # stop noisy warnings
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if debug:
        app.debug = debug
        if sqlalchemy:
            app.config['SQLALCHEMY_ECHO'] = True

    # config_module can act as defaults-setter, with overrides in env var-set config
    if config_module:
        app.config.from_object(config_module)
    if os.getenv("FLASKAPP_CONFIG", False):
        # do not fail silently if configured file cannot be loaded
        app.config.from_envvar("FLASKAPP_CONFIG", silent=False)

    # enable profiling?
    if profiler:
        app.config["PROFILE"] = True
        pstat_dir = profiler_datadir or tempfile.mkdtemp()
        log.debug("PROFILER writing pstat files to {}".format(pstat_dir))
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir=pstat_dir)

    # Do not enable the ProxyFix without reading & understanding the manual
    # https://flask.palletsprojects.com/en/stable/deploying/proxy_fix/
    # hardcoded for one level of reverse proxy only
    if proxy_fix:
        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
        )

    @app.route('/heartbeat')
    def heartbeat():
        return jsonify({"{}-server".format(import_name): "ok"})

    # ideally served directly from nginx/whatever but to avoid 404s in dev
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(STATIC_DIR, 'favicon.ico',
                                   mimetype='image/vnd.microsoft.icon')

    return app

