from logging import getLogger

# FlaskAppArgParser imported in case needs customizations/for convenience of caller
from pyapi.flask.app import FlaskAppArgParser, configured_app as base_app  # noqa # pylint: disable=unused-import
from pyapi.flask.blueprints import FlaskAPIv1

log = getLogger(__name__)


def configured_app(import_name, debug=False, config_module=None,
                   profile=False, proxy_fix=False):
    app = base_app(import_name, debug=debug, config_module=config_module,
                   profile=profile, proxy_fix=proxy_fix)
    app.register_blueprint(FlaskAPIv1)
    log.debug("configured_app: {}".format(app))
    return app

