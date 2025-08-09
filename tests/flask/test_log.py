import logging
import pytest

from flask.logging import default_handler

from pyapi.flask.api import configured_app
from pyapi.flask.log import add_flask_log_handler
from pyapi.testing.base import PyAPITestCase
from pyapi.testing.fixtures import mock_stderr


class TestFlaskLog(PyAPITestCase):

    def tearDown(self):
        for handler in logging.getLogger().handlers:
            logging.getLogger().removeHandler(handler)
        self.app.logger.removeHandler(default_handler)


    def _get_configured_app(self, app_name="testapi", **kwargs):
        self.app = configured_app(app_name, **kwargs)
        self.client = self.app.test_client()


    def test_debug_log(self):
        with mock_stderr() as _stderr:
            _ = add_flask_log_handler("testdebug", debug=True)
            self._get_configured_app()
            # logging direct to flask logger appears in log
            self.app.logger.info("flask logger info")
            # logging to root logger appears in log
            log = logging.getLogger()
            log.debug("hello world")
            # logging to __file__ log propagates to root logger
            log = logging.getLogger(__file__)
            log.info("hallo welt")
            self.client.get('/heartbeat')
        contents = self.getFhContents(_stderr)

        expect = 'DEBUG in log: add_flask_log_handler: logging configured @ level 10'
        self.assertTrue(expect in contents)

        expect = 'INFO in test_log: flask logger info'
        self.assertTrue(expect in contents)

        expect = 'INFO in test_log: hallo welt'
        self.assertTrue(expect in contents)

        expect = 'DEBUG in test_log: hello world'
        self.assertTrue(expect in contents)


    def test_info_log(self):
        with mock_stderr() as _stderr:
            _ = add_flask_log_handler("testinfo")  # default is debug=False
            self._get_configured_app()
            self.app.logger.info("flask logger info")
            self.client.get('/heartbeat')
        contents = self.getFhContents(_stderr)

        expect = 'INFO in test_log: flask logger info'
        self.assertTrue(expect in contents)

        expect_not = 'DEBUG in log: add_flask_log_handler: logging configured @ level 10'
        self.assertFalse(expect_not in contents)

