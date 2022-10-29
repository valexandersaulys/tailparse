from io import TextIOWrapper, BytesIO
import re

from . import nginx


def get_regexp_format(input_format: str = "nginx"):
    input_format = input_format.lower()
    if input_format == "nginx":
        return nginx.get_regexp_format()
    else:
        raise ValueError(
            "Unknown input_format passed: '%s'. Valid values include: ['nginx']"
            % input_format
        )


def convert_text(
    log_file: TextIOWrapper = TextIOWrapper(BytesIO(b"")), input_format: str = "nginx"
):
    regex, type_conversions, dtypes = get_regexp_format(input_format)
    L = []
    for line in log_file.readlines():
        try:
            m = re.match(regex, line)
            if m is None:
                raise ValueError(
                    "Log line did not match format '%s': '%s'" % (input_format, line)
                )
            tmp_group_dict = m.groupdict()
            # perform conversions if called for
            if type_conversions:
                tmp_items = tmp_group_dict.items()
                for k, v in tmp_items:
                    tmp_group_dict[k] = dtypes[v] if v in dtypes else str(v)
            L.append(tmp_group_dict)

        # skip over any line that doesn't conform
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
