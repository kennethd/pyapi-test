import json
import sys

import pytest

from pyapi.flask.api import configured_app
from pyapi.testing.base import PyAPITestCase

CONTENT_TYPE_TEXT_HTML = 'text/html; charset=utf-8'
CONTENT_TYPE_TEXT_PLAIN = 'text/plain; charset=utf-8'

class TestFlaskApi(PyAPITestCase):

    @classmethod
    def _get_configured_app(cls, app_name="testapi", **kwargs):
        app = configured_app(app_name, **kwargs)
        client = app.test_client()
        return (app, client)


    def test_hello(self):
        _, client = self._get_configured_app()

        response = client.get('/v1/hello')
        expect = 'Hello World!'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, CONTENT_TYPE_TEXT_PLAIN)
        self.assertEqual(response.text, expect)

        response = client.get('/v1/hello?name=Zippy')
        expect = 'Hello Zippy!'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, CONTENT_TYPE_TEXT_PLAIN)
        self.assertEqual(response.text, expect)

        response = client.post('/v1/hello', data={'name': 'Zippy'})
        expect = 'Hello Zippy!'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, CONTENT_TYPE_TEXT_PLAIN)
        self.assertEqual(response.text, expect)

        # v2 upgrades response to HTML
        response = client.get('/v2/hello')
        expect = '<blink>Hello World!</blink>'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, CONTENT_TYPE_TEXT_HTML)
        self.assertEqual(response.text, expect)

