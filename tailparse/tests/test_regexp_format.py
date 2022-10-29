import datetime
import unittest

from tailparse.log_formats import get_regexp_format
from tailparse.log_formats.nginx import get_regexp_format as nginx_format


class FormatRegexpTests(unittest.TestCase):
    def test_nginx_format(self):
        regex, type_conversions, dtypes = get_regexp_format("nginx")
        self.assertIsInstance(regex, str)
        self.assertIsInstance(type_conversions, dict)
        self.assertIsInstance(dtypes, dict)

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            get_regexp_format("egah")


if __name__ == "__main__":
    unittest.main()
