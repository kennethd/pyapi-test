from flask import jsonify

from pyapi.flask.app import configured_app
from pyapi.flask.decorators import require_https
from pyapi.testing.base import PyAPITestCase

class TestFlaskDecorators(PyAPITestCase):

    def setUp(self):
        self.app = configured_app("testapp")
        self.client = self.app.test_client()

    def test_require_https(self):
        @self.app.route('/https-only')
        @require_https
        def https_only():
            return jsonify({"https-required": True})

        response = self.client.get('/https-only', base_url='https://localhost')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/https-only', base_url='http://localhost')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], 'https://localhost/https-only')

