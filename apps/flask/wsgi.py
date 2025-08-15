import os

from pyapi.flask.api import configured_app, FlaskApiArgParser
from pyapi.flask.log import add_flask_log_handler

APP_NAME = os.environ.get('WSGI_APP_NAME', 'uwsgi-flask')
APP_PORT = os.environ.get('WSGI_APP_PORT', '9099')
DEBUG = os.environ.get('WSGI_APP_DEBUG', False)
PROFILER = os.environ.get('WSGI_APP_PROFILER_DATADIR', '/tmp')

wsgi_args = [
    f"--port={APP_PORT}",
    "--proxy-fix",  # we are deploying behind nginx reverse proxy
]
if DEBUG:
    wsgi_args.append("--debug")
if PROFILER:
    wsgi_args.append("--profiler")

args = FlaskApiArgParser.parse_args(wsgi_args)
log = add_flask_log_handler(APP_NAME, args.debug)
log.info(f"Active virtualenv is {os.environ['VIRTUAL_ENV']}")
log.info(f"args: {args}")
application = configured_app(APP_NAME)
