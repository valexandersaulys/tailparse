import re

from . import nginx


def get_regexp_format(input_format: str):
    input_format = input_format.lower()
    if input_format == "nginx":
        return nginx.get_regexp_format()
    else:
        raise ValueError(
            "Unknown input_format passed: '%s'. Valid values include: ['nginx']"
            % input_format
        )


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
    return L, table_creation_query, insertion_string, dtypes
