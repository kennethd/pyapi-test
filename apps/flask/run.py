#!/usr/bin/env python3
import os
import sys

# developer app server, only suitable for running on local machine during development

if not os.environ.get("VIRTUAL_ENV"):
    sys.exit("No active virtualenv")

from pyapi.flask.api import configured_app, FlaskApiArgParser
# instantiate a STDERR console logger from app.py for devs
from pyapi.flask.log import add_flask_log_handler

APP_NAME = 'flaskapi'

args = FlaskApiArgParser.parse_args()
log = add_flask_log_handler(APP_NAME, args.debug)
log.info(f"Active virtualenv is {os.environ['VIRTUAL_ENV']}")
log.debug(f"args: {args}")

app = configured_app(APP_NAME, debug=args.debug, proxy_fix=args.proxy_fix,
                     profiler=args.profiler, profiler_datadir=args.profiler_datadir)
log.debug(f"app: {app}")

if args.https:
    app.run(port=args.port, ssl_context=(args.ssl_crt, args.ssl_key))
else:
    app.run(port=args.port, host="0.0.0.0")
