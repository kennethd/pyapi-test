import os

from pyapi.flask.api import configured_app
from pyapi.flask.log import add_flask_log_handler

# env vars set via uwsgi vassal .ini or overridden by setting in docker env
APP_NAME = os.environ['WSGI_APP_NAME']  # Fail w/KeyError if not present
APP_PORT = os.environ['WSGI_APP_PORT']  # Fail w/KeyError if not present
DEBUG = os.environ.get('WSGI_APP_DEBUG', False)
PROFILER = os.environ.get('WSGI_APP_PROFILER', False)
PROFILER_DATADIR = os.environ.get('WSGI_APP_PROFILER_DATADIR', '')

wsgi_kwargs = {
    "port": APP_PORT,
    "proxy_fix": True,  # we are deploying behind nginx reverse proxy
}

if DEBUG:
    log.info(f"Enabling debug mode for {APP_NAME}")
    wsgi_kwargs["debug"] = True

if PROFILER:
    log.info(f"Enabling profiler for {APP_NAME}")
    wsgi_kwargs["profiler"] = True
    wsgi_kwargs["profiler_datadir"] = PROFILER_DATADIR

log = add_flask_log_handler(APP_NAME, DEBUG)
log.info(f"Active virtualenv is {os.environ['VIRTUAL_ENV']}")
application = configured_app(APP_NAME, **wsgi_args)
log.info(f"application instantiated {application}")
