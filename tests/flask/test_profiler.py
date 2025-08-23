import os

import pytest

from pyapi.flask.app import configured_app
from pyapi.testing.base import PyAPITestCase
from pyapi.testing.fixtures import tmpdir


APP_NAME = "test-flaskapp"

class TestFlaskProfiler(PyAPITestCase):

    @classmethod
    def _get_configured_app(cls, **kwargs):
        app = configured_app(APP_NAME, **kwargs)
        client = app.test_client()
        return (app, client)

    def test_profiler(self):
        with tmpdir() as pstat_dir:
            kwargs = {
                "profiler": True,
                "profiler_datadir": pstat_dir,
            }
            app, client = self._get_configured_app(**kwargs)
            self.assertTrue(app.config["PROFILE"])

            response = client.get("/heartbeat")
            # verify response was received
            self.assertEqual(response.status_code, 200)
            expect = {f"{APP_NAME}-server": "ok"}
            self.assertEqual(response.json, expect)

            # pstat_files = ['GET.heartbeat.2ms.1755963418.prof']
            pstat_files = os.listdir(pstat_dir)
            self.assertEqual(1, len(pstat_files))
            pstat_filename = pstat_files[0]
            pstat_regex = r"GET\.heartbeat\.\dms\.\d+\.prof"
            self.assertRegex(pstat_filename, pstat_regex)


    def test_no_profiler(self):
        with tmpdir() as pstat_dir:
            kwargs = {
                "profiler": False,
                "profiler_datadir": pstat_dir,
            }
            app, client = self._get_configured_app(**kwargs)
            self.assertFalse(app.config.get("PROFILE", False))

            response = client.get("/heartbeat")
            # verify response was received
            self.assertEqual(response.status_code, 200)
            expect = {f"{APP_NAME}-server": "ok"}
            self.assertEqual(response.json, expect)

            pstat_files = os.listdir(pstat_dir)
            self.assertEqual(0, len(pstat_files))

