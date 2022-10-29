import unittest

from tailparse.execute import execute_query
from tailparse.logparser import logparse
from tailparse.print_output import print_output


class SmokeTests(unittest.TestCase):
    def test_one(self):
        self.assertEqual(1 + 1, 2)

    def test_two(self):
        self.assertNotEqual(2 + 2, 5, "Stalin big mad")


if __name__ == "__main__":
    unittest.main()
