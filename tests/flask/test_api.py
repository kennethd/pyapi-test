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

        expect = 'Hello World!'
        response = client.get('/v1/hello')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, CONTENT_TYPE_TEXT_PLAIN)
        self.assertEqual(response.text, expect)

        expect = 'Hello Zippy!'
        response = client.get('/v1/hello?name=Zippy')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, CONTENT_TYPE_TEXT_PLAIN)
        self.assertEqual(response.text, expect)
        # also accepts `name` via POST
        response = client.post('/v1/hello', data={'name': 'Zippy'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, CONTENT_TYPE_TEXT_PLAIN)
        self.assertEqual(response.text, expect)

        # v2 upgrades response to HTML from 1996
        expect = '<blink>Hello World!</blink>'
        response = client.get('/v2/hello')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, CONTENT_TYPE_TEXT_HTML)
        self.assertEqual(response.text, expect)

        expect = '<blink>Hello Zippy!</blink>'
        response = client.get('/v2/hello?name=Zippy')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, CONTENT_TYPE_TEXT_HTML)
        self.assertEqual(response.text, expect)
        # also accepts `name` via POST
        response = client.post('/v2/hello', data={'name': 'Zippy'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, CONTENT_TYPE_TEXT_HTML)
        self.assertEqual(response.text, expect)

