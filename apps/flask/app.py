#!/usr/bin/env python3
import os
import sys

# developer app server, suitable for running on local machine during development

if not os.environ.get("VIRTUAL_ENV"):
    sys.exit("No active virtualenv")

from pyapi.flask.api import configured_app, FlaskAppArgParser
# instantiate a STDERR console logger from app.py for devs
from pyapi.flask.log import get_flask_logger

APP_NAME = 'flaskapi'

log = get_flask_logger(APP_NAME)
log.info(f"Active virtualenv is {os.environ['VIRTUAL_ENV']}")

args = FlaskAppArgParser.parse_args()
log.debug(f"args: {args}")

app = configured_app(APP_NAME, debug=args.debug, config_module=args.config,
                     profiler=args.profiler, proxy_fix=args.proxy_fix)
log.debug(f"app: {app}")

if args.https:
    app.run(port=args.port, ssl_context=(args.ssl_crt, args.ssl_key))
else:
    app.run(port=args.port, host="0.0.0.0")
