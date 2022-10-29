from io import TextIOWrapper, BytesIO
import os
import pprint
import sqlite3
import sys

from tailparse.log_formats import convert_text
from tailparse.print_output import print_output


pp = pprint.PrettyPrinter(indent=2)


def execute_query(
    log_file: TextIOWrapper = TextIOWrapper(BytesIO(b"")),
    input_format: str = "nginx",
    query: str = "",
    query_file: TextIOWrapper = TextIOWrapper(BytesIO(b"")),
    max_rows: int = 20,
    save_db: str = "",
    print_columns: bool = False,
) -> str:
    """
    Execute a query and return as a string

    :param log_file: _
    :param input_format: _
    :param query: _
    :param query_file: _
    :param max_rows: Max rows to display.
    :param save_db: if a valid path, whether to use an on-disk database for querying.
    :param print_columns: if True, prints to screen
    """
    # massage data into useful python structures
    dict_list, table_creation_query, insertion_string, dtypes = convert_text(
        log_file=log_file, input_format=input_format
    )

    if log_file == "":
        raise ValueError("No Log File Provided")
    if query == "" and query_file == "" and not print_columns:
        raise ValueError("Did not pass in a query or query_file")

    if print_columns:
        return pp.pformat(dtypes) + "\n"

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

    to_ret = ""
    # execute the passed query
    if query:
        query = " ".join(query.split("\n"))
        try:
            executed_query = curr.execute(query)
        except sqlite3.OperationalError:
            raise
        if max_rows == 0:
            tmpt = list(executed_query)
        else:
            tmpt = list(row for i, row in enumerate(executed_query) if i < max_rows)
        column_names = list(map(lambda x: x[0], curr.description))
        to_ret += print_output(list_of_results=tmpt, column_names=column_names)

    elif query_file:
        for query in query_file.read().split("\n"):
            if query.strip() == "":
                continue
            try:
                executed_query = curr.execute(query)
            except sqlite3.OperationalError:
                raise
            if max_rows == 0:
                tmpt = list(executed_query)
            else:
                tmpt = list(row for i, row in enumerate(executed_query) if i < max_rows)
            to_ret += "> " + query.strip()
            to_ret += "\n"
            to_ret += print_output(
                list_of_results=tmpt,
                column_names=list(map(lambda x: x[0], curr.description)),
            )
            to_ret += "\n\n"

    return to_ret.strip() + "\n"
