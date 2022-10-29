import unittest

from tailparse.execute import execute_query
from tailparse.print_output import print_output


def foo():
    return


class SmokeTests(unittest.TestCase):
    def test_one(self):
        self.assertEqual(1 + 1, 2)

    def test_two(self):
        self.assertNotEqual(2 + 2, 5, "Stalin big mad")

    def test_three(self):
        self.assertIsInstance(execute_query, type(foo))
        self.assertIsInstance(print_output, type(foo))


if __name__ == "__main__":
    unittest.main()
