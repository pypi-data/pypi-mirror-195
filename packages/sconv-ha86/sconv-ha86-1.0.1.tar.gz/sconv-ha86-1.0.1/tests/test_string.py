import unittest

from sconv import sconv

class Test(unittest.TestCase):
    def test_lower_method(self):
        self.assertEqual(sconv.lower("TEST"), "test")
        self.assertNotEqual(sconv.lower("test"), "TEST")

    def test_upper_method(self):
        self.assertEqual(sconv.upper("test"), "TEST")
        self.assertNotEqual(sconv.upper("TEST"), "test")

    def test_title_method(self):
        self.assertEqual(sconv.title("hello world"), "Hello World")
        self.assertNotEqual(sconv.title("hELLO wORLD"), "hello world")