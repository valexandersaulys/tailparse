import argparse
import sys

from tailparse import __version__
from tailparse.execute import execute_query


def cli():
    parser = argparse.ArgumentParser(description="Process logs as if they were SQL.")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s v{version}".format(version=__version__),
    )
    parser.add_argument(
        "-p",
        "--print",
        default=False,
        help="Print out the requisite columns",
        action="store_true",
        dest="print_columns",
    )
    parser.add_argument(
        "-i",
        "--input-format",
        default="nginx",
        required=False,
        help="""
        The format of the log we're processing. Defaults to 'nginx'. Options 
        include ['nginx']
        """,
    )
    parser.add_argument(
        "-q",
        "--query",
        required=False,
        help="""
        The query to execute. Don't include any 'FROM' statement as this is 
        added automatically. If not included, make sure to include a -f/--file 
        arugmenet
        """,
    )
    parser.add_argument(
        "-r",
        "--max-rows",
        type=int,
        default=20,
        help="Number of max rows to print. Defaults to 20. Put 0 to print all.",
    )
    parser.add_argument(
        "-s",
        "--save-db",
        type=str,
        default="",
        help="""Whether to save the resulting SQLite data file. Defaults to 
        not saving it and using ':memory:' instead. If the database exists, 
        then the log file will not be used to populate it and instead it will 
        be read from. This can be helpful if you're running a lot of queries
        as the log file doesn't need to be re-parsed everytime.
        """,
    )
    parser.add_argument(
        "log_file",
        metavar="logs",
        nargs="?",
        type=argparse.FileType("r"),
        default=(None if sys.stdin.isatty() else sys.stdin),
        help="The path to the input log we're processing. If not present, will use stdin.",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=argparse.FileType("r"),
        help="""
        Execute multiple queries contained with a file. Can be used in place 
        of -q/--query
        """,
    )
    args = parser.parse_args()
    if args.log_file is None:
        sys.stdout.write("ERROR: Must provide log file either as path or via stdin\n")
        exit(1)
    text = execute_query(
        log_file=args.log_file,
        input_format=args.input_format,
        query=args.query,
        query_file=args.file,
        max_rows=int(args.max_rows),
        save_db=args.save_db,
        print_columns=args.print_columns,
    )
    sys.stdout.write(text)
