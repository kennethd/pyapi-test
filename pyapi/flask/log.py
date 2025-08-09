#
#                               README
#
# The logger defined here is intended to be imported into the entrypoint of a
# process; either `app.py`, `wsgi.py`, or possibly a command line script, and
# is intended for one-time configuration of app logging behavior
#
# Almost all code should use the standard python logging interface:
#
#    import logging
#    log = logging.getLogger(__name__)
#    log.info("This message will find its way to the correct handlers")
#
# Which is to say, please do not import the logger defined here, unless you
# are sure you know that it is the right thing to do.
#
import logging
import os

from flask.logging import default_handler


log = logging.getLogger(__name__)


def add_flask_log_handler(name, debug=False):
    if debug:
        level = logging.DEBUG
    else:
        level = logging.INFO
    default_handler.setLevel(level)

    # instead of app-specific logger, just add flask handler to root logger
    # https://flask.palletsprojects.com/en/stable/logging/#other-libraries
    #log = logging.getLogger(name)
    #log.setLevel(level)
    #log.addHandler(default_handler)

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(default_handler)

    log.debug(f'add_flask_log_handler: logging configured @ level {level}')
    return log

