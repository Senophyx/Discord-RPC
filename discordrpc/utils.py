import time
import datetime

# Credits to qwertyquerty
# https://github.com/qwertyquerty/pypresence/blob/master/pypresence/utils.py#L12C1-L21C13

def remove_none(d: dict):
    for item in d.copy():
        if isinstance(d[item], dict):
            if len(d[item]):
                d[item] = remove_none(d[item])
            if not len(d[item]):
                del d[item]
        elif d[item] is None:
            del d[item]
    return d


timestamp = int(time.mktime(time.localtime()))


def date_to_timestamp(date:str):
    return int(time.mktime(
        datetime.datetime.strptime(date, "%d/%m/%Y-%H:%M:%S").timetuple()
    ))