import os
import shutil
import sys

from pyapi.testing.base import PyAPITestCase
from pyapi.testing.fixtures import mock_stderr, mock_stdout, tmpdir

class TestTestFixtures(PyAPITestCase):

    def test_tmpdir(self):
        with tmpdir() as dirpath:
            self.assertTrue(os.path.exists(dirpath))
        self.assertFalse(os.path.exists(dirpath))

        try:
            with tmpdir(cleanup=False) as dirpath:
                self.assertTrue(os.path.exists(dirpath))
            # directory was not removed @ end of context
            self.assertTrue(os.path.exists(dirpath))
        finally:
            shutil.rmtree(dirpath)

    def test_mock_stderr(self):
        orig_stderr = sys.stderr
        with mock_stderr() as _stderr:
            print("Test STDERR", file=sys.stderr)
            # orig_stderr has no .getvalue() method
            self.assertEqual(_stderr.getvalue().strip(), "Test STDERR")
            self.assertNotEqual(orig_stderr.fileno, sys.stderr.fileno)
        self.assertEqual(orig_stderr.fileno, sys.stderr.fileno)

    def test_mock_stdout(self):
        orig_stdout = sys.stdout
        with mock_stdout() as _stdout:
            print("Test STDOUT")
            # orig_stdout has no .getvalue() method
            self.assertEqual(_stdout.getvalue().strip(), "Test STDOUT")
            self.assertNotEqual(orig_stdout.fileno, sys.stdout.fileno)
        self.assertEqual(orig_stdout.fileno, sys.stdout.fileno)

