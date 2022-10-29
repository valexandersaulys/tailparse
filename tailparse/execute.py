import os
import pprint
import sqlite3

from tailparse.log_formats import convert_text
from tailparse.print_output import print_output


pp = pprint.PrettyPrinter(indent=2)


def execute_query(
    log_file_path: str = "",
    input_format: str = "nginx",
    query: str = "",
    query_file: str = "",
    max_rows: int = 20,
    save_db: bool = False,
    print_columns: bool = False,
) -> str:
    # massage data into useful python structures
    dict_list, table_creation_query, insertion_string, dtypes = convert_text(
        filepath=log_file_path, input_format=input_format
    )

    if log_file_path == "":
        raise ValueError("No Log File Provided")
    if query == "" and query_file == "":
        raise ValueError("Did not pass in a query or query_file")

    # dump to SQLite3
    already_exists = False
    if save_db:
        already_exists = os.path.exists(save_db)
        conn = sqlite3.connect(save_db)
        curr = conn.cursor()
    else:
        conn = sqlite3.connect(":memory:")

    if save_db == "" or not already_exists:
        curr = conn.cursor()
        conn.commit()
        curr.execute(table_creation_query)
        curr.executemany(insertion_string, dict_list)
        conn.commit()

    if print_columns:
        sys.stdout.write(pp.pformat(dtypes))
        sys.stdout.write("\n")

    to_ret = ""
    # execute the passed query
    if query:
        query = " ".join(query.split("\n"))
        executed_query = curr.execute(query)
        if max_rows == 0:
            tmpt = list(executed_query)
        else:
            tmpt = list(row for i, row in enumerate(executed_query) if i < max_rows)
        column_names = list(map(lambda x: x[0], curr.description))
        to_ret += print_output(list_of_results=tmpt, column_names=column_names)

    elif query_file:
        with open(query_file, "r") as f:
            for query in f.readlines():
                executed_query = curr.execute(query)
                if max_rows == 0:
                    tmpt = list(executed_query)
                else:
                    tmpt = list(
                        row for i, row in enumerate(executed_query) if i < max_rows
                    )
                column_names = list(map(lambda x: x[0], curr.description))
                to_ret += "> " + query.strip()
                to_ret += "\n"
                to_ret += print_output(list_of_results=tmpt, column_names=column_names)
                to_ret += "\n\n"

    # remove last \n\n
    return to_ret.strip() + "\n"
