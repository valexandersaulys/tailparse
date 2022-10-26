#!/usr/bin/env python3.10
import argparse
import re
import sqlite3
import sys

import pandas as pd


pd.set_option("display.width", None)
pd.set_option("max_colwidth", None)


def get_regexp_format(input_format):
    conf = '$ip - $user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"'
    regex = "".join(
        "(?P<" + g + ">.*?)" if g else re.escape(c)
        for g, c in re.findall(r"\$(\w+)|(.)", conf)
    )
    return regex


def convert_text(filepath, input_format):
    regex = get_regexp_format(input_format)
    L = []
    with open(filepath, "r") as f:
        for line in f.readlines():
            try:
                m = re.match(regex, line)
                L.append(m.groupdict())
            except:
                continue
    df = pd.DataFrame(L)
    return df


def main():
    # TODO: print out the full query with no limits or formatting
    parser = argparse.ArgumentParser(description="Process some SQL")
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
        help="The format of the log we're processing. Defaults to 'nginx'. Options include ['nginx']",
    )
    parser.add_argument(
        "-q",
        "--query",
        required=True,
        help="The query to execute. Don't include any 'FROM' statement as this is added automatically.",
    )
    parser.add_argument(
        "-r",
        "--max-rows",
        type=int,
        default=20,
        help="Number of max rows to print. Defaults to 20. Put 0 to print all.",
    )
    parser.add_argument(
        "-c",
        "--max-cols",
        type=int,
        default=10,
        help="Number of max columns to print. Defaults to 10. Put 0 to print all.",
    )
    parser.add_argument(
        "log_file_path",
        metavar="LOGS_TO_QUERY",
        type=str,
        help="The path to the input log we're processing. If not present, will use stdin.",
    )
    args = parser.parse_args()

    if args.max_rows == 0:
        pd.set_option("display.max_rows", None)
    else:
        pd.set_option("display.max_rows", int(args.max_rows))

    if args.max_cols == 0:
        pd.set_option("display.max_columns", None)
    else:
        pd.set_option("display.max_columns", int(args.max_rows))

    df = convert_text(filepath=args.log_file_path, input_format=args.input_format)
    conn = sqlite3.connect(":memory:")
    df.to_sql(name="logs", con=conn)

    if args.print_columns:
        print("\n".join(df.columns.tolist()))
        return

    query = " ".join(args.query.split("\n"))
    # query += " FROM logs"
    try:
        tmpt = pd.read_sql_query(sql=query, con=conn)
        print(tmpt)
    except pd.errors.DatabaseError:
        print("Invalid SQL -- did you forget the 'FROM logs' in the query?")


if __name__ == "__main__":
    main()
