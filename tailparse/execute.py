import os
import pprint
import sqlite3

from tailparse.log_formats import convert_text


pp = pprint.PrettyPrinter(indent=2)


def execute_query(args) -> str:
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

    to_ret = ""
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
        to_ret += pp.pformat(names)
        to_ret += pp.pformat(tmpt)

    elif args.file:
        to_ret = "\n"
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
                to_ret += query.strip()
                to_ret += pp.pformat(names)
                to_ret += pp.pformat(tmpt)
                to_ret += "\n"

    to_ret += "\n"
    return to_ret
