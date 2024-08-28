import time
from datetime import datetime, UTC

# Credits to qwertyquerty
# https://github.com/qwertyquerty/pypresence/blob/master/pypresence/utils.py#L12C1-L21C13


def get_timestamp() -> int:
    return int(datetime.now(tz=UTC).timestamp())


def remove_none(d: dict):
    for item in d.copy():
        if isinstance(d[item], dict):
            if d[item]:
                d[item] = remove_none(d[item])
            if not d[item]:
                del d[item]
        elif d[item] is None:
            del d[item]
    return d


def date_to_timestamp(date: str):
    return int(time.mktime(datetime.strptime(date, "%d/%m/%Y-%H:%M:%S").timetuple()))
