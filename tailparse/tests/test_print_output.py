import unittest

from tailparse.print_output import print_output


class PrintOutputTests(unittest.TestCase):
    def test_one(self):
        self.assertEqual(
            print_output(
                [
                    (
                        1,
                        2,
                        3,
                    )
                ],
                column_names=None,
            ),
            "1\t2\t3",
        )
        self.assertEqual(
            print_output(
                [
                    (
                        "egah",
                        2,
                        "egah",
                    )
                ],
                column_names=None,
            ),
            "egah\t2\tegah",
        )
        self.assertEqual(
            print_output(
                [
                    (
                        "egah",
                        2,
                        "egah",
                    ),
                    (
                        "ooga",
                        3,
                        "booga",
                    ),
                ],
                column_names=None,
            ),
            "egah\t2\tegah\nooga\t3\tbooga",
        )


if __name__ == "__main__":
    unittest.main()
