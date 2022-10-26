#!/usr/bin/env python3.10
import argparse
from datetime import datetime
import os
import pprint
import re
import sqlite3
import sys

pp = pprint.PrettyPrinter(indent=2)


def get_regexp_format(input_format):
    conf = '$ip - $user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"'
    regex = "".join(
        "(?P<" + g + ">.*?)" if g else re.escape(c)
        for g, c in re.findall(r"\$(\w+)|(.)", conf)
    )
    # any non-specified type_conversions default to string
    type_conversions = {
        "time_local": lambda x: datetime.strptime(x, "%d/%b/%Y:%H:%M:%S %z"),
        "status": int,
        "body_bytes_sent": int,
    }
    # dtypes is fed into SQLite for table creation
    # TODO: would CHAR(XYZ) be faster than TEXT?
    dtypes = {
        "ip": "TEXT",
        "user": "TEXT",
        "time_local": "DATETIME",
        "request": "TEXT",
        "status": "TEXT",
        "body_bytes_sent": "TEXT",
        "http_referer": "TEXT",
        "http_user_agent": "TEXT",
    }
    return regex, type_conversions, dtypes


def convert_text(filepath, input_format):
    regex, type_conversions, dtypes = get_regexp_format(input_format)
    L = []
    with open(filepath, "r") as f:
        for line in f.readlines():
            try:
                m = re.match(regex, line)
                tmp_group_dict = m.groupdict()
                # perform conversions if called for
                if type_conversions:
                    tmp_items = tmp_group_dict.items()
                    for k, v in tmp_items:
                        tmp_group_dict[k] = dtypes[v] if v in dtypes else str(v)
                L.append(tmp_group_dict)
            except:
                continue

    table_creation_strings = ["%s %s" % (k, v) for k, v in dtypes.items()]
    table_creation_query = """
    CREATE TABLE logs (
        -- ID INT PRIMARY KEY     NOT NULL,
        %s
    );
    """ % (
        ",\n".join(table_creation_strings)
    )
    tmp = ", ".join(":%s" % dtype for dtype, _ in dtypes.items())
    insertion_string = "INSERT INTO logs VALUES (%s)" % tmp
    return L, table_creation_query, insertion_string


def logparse(parser):
    # TODO: print out the full query with no limits or formatting
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
        "log_file_path",
        metavar="LOGS_TO_QUERY",
        type=str,
        help="The path to the input log we're processing. If not present, will use stdin.",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="""
        Execute multiple queries contained with a file. Can be used in place 
        of -q/--query
        """,
    )
    args = parser.parse_args()

    # massage data into useful python structures
    dict_list, table_creation_query, insertion_string = convert_text(
        filepath=args.log_file_path, input_format=args.input_format
    )

    # dump to SQLite3
    if args.save_db:
        already_exists = os.path.exists(args.save_db)
        conn = sqlite3.connect(args.save_db)
        curr = conn.cursor()
    else:
        conn = sqlite3.connect(":memory:")

    if args.save_db == "" or not already_exists:
        curr = conn.cursor()
        conn.commit()
        curr.execute(table_creation_query)
        curr.executemany(insertion_string, dict_list)
        conn.commit()

    # execute the passed query
    if args.query:
        query = " ".join(args.query.split("\n"))
        executed_query = curr.execute(query)
        if args.max_rows == 0:
            tmpt = list(executed_query)
        else:
            tmpt = list(
                row for i, row in enumerate(executed_query) if i < args.max_rows
            )

        names = list(map(lambda x: x[0], curr.description))
        pp.pprint(names)
        pp.pprint(tmpt)

    elif args.file:
        print("")
        with open(args.file, "r") as f:
            for query in f.readlines():
                executed_query = curr.execute(query)
                if args.max_rows == 0:
                    tmpt = list(executed_query)
                else:
                    tmpt = list(
                        row for i, row in enumerate(executed_query) if i < args.max_rows
                    )
                names = list(map(lambda x: x[0], curr.description))
                print(query.strip())
                pp.pprint(names)
                pp.pprint(tmpt)
                print("")


if __name__ == "__main__":
    main()
