import sys

from pyapi.testing.base import PyAPITestCase
from pyapi.testing.fixtures import mock_stderr, mock_stdout

class TestBasePyAPITestCase(PyAPITestCase):

    def test_assert_fh_contains(self):
        with mock_stdout() as _stdout:
            print("Hello!")
            self.assertFhContains(_stdout, "Hello!")
        # it still works after _stdout is out of scope
        self.assertFhContains(_stdout, "Hello!")

        with mock_stderr() as _stderr:
            print("Goodbye!", file=sys.stderr)
        self.assertFhContains(_stderr, "Goodbye!")

    def test_assert_fh_equals(self):
        with mock_stdout() as _stdout:
            print("Hello!")
        self.assertFhEquals(_stdout, "Hello!\n")

        with mock_stderr() as _stderr:
            print("Goodbye!", file=sys.stderr)
        self.assertFhEquals(_stderr, "Goodbye!\n")

