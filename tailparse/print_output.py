from typing import List, Optional, Tuple


def print_output(list_of_results: List[Tuple[str]], column_names: Optional[List[str]]):
    """
    Format the outputs involved:

    :param list_of_results:
    """
    to_ret = ""
    if column_names:
        to_ret += "\t".join(column_names)
        to_ret += "\n"

    to_append = []
    for result in list_of_results:
        tmp = "\t".join(str(x) for x in result)
        to_append.append(tmp)
    to_ret += "".join(to_append)
    return to_ret
