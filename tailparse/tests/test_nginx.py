import os
import sqlite3
import unittest

from tailparse.execute import execute_query
from tailparse.print_output import print_output


class NginxTests(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.log_file = open("tailparse/tests/test-nginx-logs.txt", "r")
        self.default_args = {
            "log_file": self.log_file,
            "input_format": "nginx",
            "query_file": "",
            "max_rows": 20,
            "save_db": "",
            "print_columns": False,
        }
        self.query_file_path = "/tmp/test-query.sql"
        self.query_file = open(self.query_file_path, "w+")
        self.query_file.write(
            "SELECT MAX(time_local), MIN(time_local) FROM logs\nSELECT COUNT(*) FROM logs\nSELECT COUNT(*) FROM logs"
        )
        self.query_file.seek(0)

    def tearDown(self):
        self.log_file.close()
        self.query_file.close()
        os.remove(self.query_file_path)
        if os.path.exists("/tmp/tmp.sqlite3.db"):
            os.remove("/tmp/tmp.sqlite3.db")

    def test_query_one(self):
        query = "SELECT * FROM logs LIMIT 1"
        response = execute_query(query=query, **self.default_args).strip()
        self.assertEqual(len(response.split("\n")), 2)
        self.assertEqual(
            response.split("\n")[0],
            "ip\tuser\ttime_local\trequest\tstatus\tbody_bytes_sent\thttp_referer\thttp_user_agent",
        )
        self.assertEqual(
            response.split("\n")[1],
            "24.90.87.23\t-\t12/Oct/2022:01:42:44 +0000\tGET /css/output.min.css HTTP/1.1\t200\t80784\thttps://example.com/lists\tMozilla/5.0 (iPhone; CPU iPhone OS 16_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        )

    def test_query_two(self):
        query = "SELECT * FROM logs LIMIT 2"
        response = execute_query(query=query, **self.default_args).strip()
        self.assertEqual(len(response.split("\n")), 3)
        self.assertEqual(
            response.split("\n")[0],
            "ip\tuser\ttime_local\trequest\tstatus\tbody_bytes_sent\thttp_referer\thttp_user_agent",
        )
        self.assertEqual(
            response.split("\n")[1],
            "24.90.87.23\t-\t12/Oct/2022:01:42:44 +0000\tGET /css/output.min.css HTTP/1.1\t200\t80784\thttps://example.com/lists\tMozilla/5.0 (iPhone; CPU iPhone OS 16_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        )
        self.assertEqual(
            response.split("\n")[2],
            "52.141.49.83\t-\t12/Oct/2022:04:13:03 +0000\tHEAD /WORDPRESS HTTP/1.1\t404\t0\thttp://example.com/WORDPRESS\tMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        )

    def test_query_three(self):
        query = "SELECT * FROM logs"
        response = execute_query(query=query, **self.default_args).strip()
        self.assertEqual(len(response.split("\n")), 21)  # 20 + header

    def test_changed_max_rows_one(self):
        query = "SELECT * FROM logs"
        modified_args = self.default_args.copy()
        modified_args["max_rows"] = 30
        response = execute_query(query=query, **modified_args).strip()
        self.assertEqual(len(response.split("\n")), 31)

    def test_changed_max_rows_two(self):
        query = "SELECT * FROM logs"
        modified_args = self.default_args.copy()
        modified_args["max_rows"] = 0
        response = execute_query(query=query, **modified_args).strip()
        self.assertEqual(len(response.split("\n")), 51)

    def test_bad_query(self):
        query = "SELECT *"
        with self.assertRaises(sqlite3.OperationalError):
            response = execute_query(query=query, **self.default_args).strip()

    def test_query_file(self):
        query = "SELECT * FROM logs"  # query file looks different
        modified_args = self.default_args.copy()
        modified_args["query_file"] = self.query_file
        self.assertTrue(os.path.exists(self.query_file_path))
        response = execute_query(**modified_args).strip()
        self.assertEqual(
            response,
            """
> SELECT MAX(time_local), MIN(time_local) FROM logs
MAX(time_local)\tMIN(time_local)
23/Oct/2022:17:56:10 +0000\t02/Oct/2022:00:21:53 +0000

> SELECT COUNT(*) FROM logs
COUNT(*)
50

> SELECT COUNT(*) FROM logs
COUNT(*)
50
""".strip(),
        )

    def test_save_db(self):
        query = "SELECT * FROM logs"
        modified_args = self.default_args.copy()
        modified_args["save_db"] = "/tmp/tmp.sqlite3.db"
        self.assertFalse(os.path.exists("/tmp/tmp.sqlite3.db"))
        response = execute_query(query=query, **modified_args).strip()
        self.assertEqual(len(response.split("\n")), 21)
        self.assertEqual(
            response.split("\n")[0],
            "ip\tuser\ttime_local\trequest\tstatus\tbody_bytes_sent\thttp_referer\thttp_user_agent",
        )
        self.assertEqual(
            response.split("\n")[1],
            "24.90.87.23\t-\t12/Oct/2022:01:42:44 +0000\tGET /css/output.min.css HTTP/1.1\t200\t80784\thttps://example.com/lists\tMozilla/5.0 (iPhone; CPU iPhone OS 16_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        )
        self.assertTrue(os.path.exists("/tmp/tmp.sqlite3.db"))
        self.assertGreater(os.path.getsize("/tmp/tmp.sqlite3.db"), 0)

    def test_print_columns(self):
        query = ""
        modified_args = self.default_args.copy()
        modified_args["print_columns"] = True
        response = execute_query(query=query, **modified_args).strip()
        self.assertEqual(
            response,
            """
{ 'body_bytes_sent': 'TEXT',
  'http_referer': 'TEXT',
  'http_user_agent': 'TEXT',
  'ip': 'TEXT',
  'request': 'TEXT',
  'status': 'TEXT',
  'time_local': 'DATETIME',
  'user': 'TEXT'}
""".strip(),
        )


if __name__ == "__main__":
    unittest.main()
