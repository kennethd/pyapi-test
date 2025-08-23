import logging

# FlaskAppArgParser imported for convenience of caller imports
from pyapi.flask.app import FlaskAppArgParser as FlaskApiArgParser, \
                            configured_app as base_app
from pyapi.flask.blueprints import FlaskAPIv1, FlaskAPIv2


log = logging.getLogger(__name__)


def configured_app(import_name, debug=False, proxy_fix=False,
                   profiler=False, profiler_datadir=""):
    app = base_app(import_name, debug=debug, proxy_fix=proxy_fix,
                   profiler=profiler, profiler_datadir=profiler_datadir)
    app.register_blueprint(FlaskAPIv1)
    app.register_blueprint(FlaskAPIv2)
    log.debug("configured_app: {}".format(app))
    return app

