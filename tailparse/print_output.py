from typing import List, Optional, Tuple


def print_output(
    list_of_results: List[Tuple[str]], column_names: Optional[List[str]]
) -> str:
    """
    Format the outputs involved

    :param list_of_results: a list of tuples where each tuple is a row from a
        SQL query. Required.
    :param column_names: the list of column names. If None, then it will not
        print. Defaults to None.
    :returns str: to print (usually anyway)
    """
    to_ret = ""
    if column_names:
        to_ret += "\t".join(column_names)
        to_ret += "\n"

    to_append = []
    for result in list_of_results:
        tmp = "\t".join(str(x) for x in result)
        to_append.append(tmp)
    to_ret += "\n".join(to_append)
    return to_ret
