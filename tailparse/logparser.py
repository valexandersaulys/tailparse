#!/usr/bin/env python3.10
import argparse
import sys
from typing import Union

from tailparse.execute import execute_query


def logparse(
    log_file_path: str = "",
    input_format: str = "nginx",
    query: str = "",
    query_file: str = "",
    max_rows: int = 20,
    save_db: bool = False,
    print_columns: bool = False,
) -> None:
    """
    Process arguments from
    """
    to_print = execute_query(
        log_file_path=log_file_path,
        input_format=input_format,
        query=query,
        query_file=query_file,
        max_rows=max_rows,
        save_db=save_db,
        print_columns=print_columns,
    )
    sys.stdout.write(to_print)
