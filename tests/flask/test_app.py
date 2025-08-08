import argparse
import json
import sys
from unittest import mock

import pytest

from pyapi.flask.app import FlaskAppArgParser, configured_app
from pyapi.testing.base import PyAPITestCase
from pyapi.testing.fixtures import mock_stderr

ARG_DEFAULTS = {
    "debug": False,
    "config": None,
    "https": False,
    "ssl_key": "",
    "ssl_crt": "",
    "profiler": False,
    "proxy_fix": False,
}

class TestFlaskApp(PyAPITestCase):

    @classmethod
    def _get_configured_app(cls, app_name="testapp", **kwargs):
        app = configured_app(app_name, **kwargs)
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
        app, client = self._get_configured_app()
        response = client.get('/heartbeat')
        self.assertEqual(response.status_code, 200)
        expect = {"testapp-server": "ok"}
        self.assertEqual(response.json, expect)

    def test_flask_app_arg_parser(self):
        args = FlaskAppArgParser.parse_args(["--port=9999", "--debug"])
        expect = argparse.Namespace(**ARG_DEFAULTS)
        expect.port = 9999
        expect.debug = True
        #self.assertEqual(args, expect)
        # verify manually passing params to parse_args works like this too
        ##TODOargs = FlaskAppArgParser.parse_args(["--port", "9999", "--debug"])
        ##TODOself.assertEqual(args, expect)

        # don't write confusing errors to terminal output
        with mock_stderr() as _stderr:
            # missing required --port
            with mock.patch('sys.exit') as mock_exit:
                FlaskAppArgParser.parse_args()
                self.assertTrue(mock_exit.called)
                expect = "required: --port"
                self.assertTrue(expect in _stderr.getvalue().strip())

