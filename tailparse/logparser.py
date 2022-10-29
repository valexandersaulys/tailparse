#!/usr/bin/env python3.10
import argparse
from io import TextIOWrapper, BytesIO
import sys
from typing import Union

from tailparse.execute import execute_query


def logparse(
    log_file: str = "",
    input_format: str = "nginx",
    query: str = "",
    query_file: TextIOWrapper = TextIOWrapper(BytesIO(b"")),
    max_rows: int = 20,
    save_db: str = "",
    print_columns: bool = False,
) -> None:
    """
    Process arguments from argparse
    """
    to_print = execute_query(
        log_file=log_file,
        input_format=input_format,
        query=query,
        query_file=query_file,
        max_rows=max_rows,
        save_db=save_db,
        print_columns=print_columns,
    )
    sys.stdout.write(to_print)
