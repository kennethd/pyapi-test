import os

from pyapi.testing.base import PyAPITestCase
from pyapi.testing.contexts import env_var_context


class TestContexts(PyAPITestCase):

    def test_env_var_context(self):
        self.assertTrue('FOO_TEST_CONTEXT' not in os.environ)
        with env_var_context(FOO_TEST_CONTEXT='BAR'):
            self.assertTrue('FOO_TEST_CONTEXT' in os.environ)
            self.assertEqual(os.getenv('FOO_TEST_CONTEXT'), 'BAR')
        self.assertTrue('FOO_TEST_CONTEXT' not in os.environ)

    def test_env_var_context_coerces_str(self):
        self.assertTrue('FOO_TEST_CONTEXT' not in os.environ)
        with env_var_context(FOO_TEST_CONTEXT=123):
            self.assertEqual(os.getenv('FOO_TEST_CONTEXT'), '123')
        self.assertTrue('FOO_TEST_CONTEXT' not in os.environ)

