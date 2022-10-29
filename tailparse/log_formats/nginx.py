import re
from datetime import datetime


def get_regexp_format():
    conf = '$ip - $user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"'
    regex = "".join(
        "(?P<" + g + ">.*?)" if g else re.escape(c)
        for g, c in re.findall(r"\$(\w+)|(.)", conf)
    )
    # any non-specified type_conversions default to string
    type_conversions = {
        "time_local": lambda x: datetime.strptime(x, "%d/%b/%Y:%H:%M:%S %z"),
        "status": int,
        "body_bytes_sent": int,
    }
    # dtypes is fed into SQLite for table creation
    # TODO: would CHAR(XYZ) be faster than TEXT?
    dtypes = {
        "ip": "TEXT",
        "user": "TEXT",
        "time_local": "DATETIME",
        "request": "TEXT",
        "status": "TEXT",
        "body_bytes_sent": "TEXT",
        "http_referer": "TEXT",
        "http_user_agent": "TEXT",
    }
    return regex, type_conversions, dtypes
