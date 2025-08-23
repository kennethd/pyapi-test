import argparse
import json
import sys
from unittest import mock

import pytest

from pyapi.flask.app import STATIC_DIR, FlaskAppArgParser, configured_app
from pyapi.testing.base import PyAPITestCase
from pyapi.testing.fixtures import mock_stderr

ARG_DEFAULTS = {
    "debug": False,
    "config": None,
    "https": False,
    "ssl_key": "",
    "ssl_crt": "",
    "profiler": False,
    "profiler_datadir": "",
    "proxy_fix": False,
}

APP_NAME = "test-flaskapp"


class TestFlaskApp(PyAPITestCase):

    @classmethod
    def _get_configured_app(cls, **kwargs):
        app = configured_app(APP_NAME, **kwargs)
        client = app.test_client()
        return (app, client)


    def test_configured_app(self):
        app, client = self._get_configured_app()

        @app.route('/')
        def index():
            return 'hi'

        response = client.get('/')
        self.assertEqual(response.status_code, 200)


    def test_heartbeat(self):
        _, client = self._get_configured_app()
        response = client.get('/heartbeat')
        self.assertEqual(response.status_code, 200)
        expect = {f"{APP_NAME}-server": "ok"}
        self.assertEqual(response.json, expect)


    def test_factory_args_propagate_to_app(self):
        factory_args = {
            "debug": True,
            "profiler": True,
            "config_module": "pyapi.testing.config",
            "sqlalchemy": True,
            "profiler_datadir": "/tmp",
        }

        app, client = self._get_configured_app(**factory_args)
        self.assertTrue(app.debug)
        self.assertTrue(app.config["PROFILE"])
        # TEST_MODE set by pyapi.testing.config
        self.assertTrue(app.config["TEST_MODE"])
        # set by combo of DEBUG + sqlalchemy=True
        self.assertTrue(app.config["SQLALCHEMY_ECHO"])

    def test_static_folder(self):
        # verify static files are being packaged correctly with app
        app, client = self._get_configured_app()
        self.assertEqual(STATIC_DIR, app.static_folder)
        response = client.get('/favicon.ico')
        self.assertEqual(response.status_code, 200)


    def test_flask_app_arg_parser(self):
        args = FlaskAppArgParser.parse_args(["--port=9999", "--debug"])
        expect = argparse.Namespace(**ARG_DEFAULTS)
        expect.port = 9999
        expect.debug = True
        self.assertEqual(args, expect)

        # don't write confusing errors to terminal output
        with mock_stderr() as _stderr:
            # missing required --port
            with mock.patch('sys.exit') as mock_exit:
                FlaskAppArgParser.parse_args()
                self.assertTrue(mock_exit.called)
                expect = "required: --port"
                self.assertTrue(expect in _stderr.getvalue().strip())

