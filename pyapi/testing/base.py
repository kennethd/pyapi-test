import logging
import unittest


log = logging.getLogger(__name__)


class PyAPITestCase(unittest.TestCase):
    maxDiff = None


    def getFhContents(self, fh):
        """returns string

        flushes, seeks to beginning, then reads filehandle `fh` and returns contents
        """
        fh.flush()
        fh.seek(0)
        contents = fh.read()
        return contents


    def assertFhContains(self, fh, s):
        """asserts filehandle `fh` contains string `s`:

        ```
            with mock_stdout() as _stdout:
                print("hello")
            self.assertFhContains(_stdout, "hello")
        ```
        """
        log.debug("assertFhContains: ", s)
        contents = self.getFhContents(fh)
        self.assertTrue(s in contents)


    def assertFhNotContains(self, fh, s):
        """inverse of assertFhContains"""
        log.debug("assertFhNotContains: ", s)
        contents = self.getFhContents(fh)
        self.assertFalse(s in contents)


    def assertFhEquals(self, fh, s):
        """asserts filehandle `fh` contains string `s` exactly:

        ```
            with mock_stdout() as _stdout:
                print("hello")
            self.assertFhEquals(_stdout, "hello\\n")
        ```
        """
        log.debug("assertFhEquals: ", s)
        contents = self.getFhContents(fh)
        self.assertEqual(s, contents)


    def assertFhNotEquals(self, fh, s):
        """inverse of assertFhEquals"""
        log.debug("assertFhNotEquals: ", s)
        contents = self.getFhContents(fh)
        self.assertNotEqual(s, contents)

