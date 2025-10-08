import time
from datetime import datetime
from .exceptions import *

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
        datetime.strptime(date, "%d/%m/%Y-%H:%M:%S").timetuple()
    ))

def use_local_time():
    now = datetime.now()
    seconds_since_midnight = now.hour * 3600 + now.minute * 60 + now.second
    return {
        "ts_start": int(time.time()) - seconds_since_midnight
    }

def ProgressBar(current:int, duration:int) -> dict:
    if int(current) > int(duration):
        raise ProgressbarError("Current cannot exceed Duration")
    
    current_time = int(time.time()) - int(current)
    finish_time = current_time + int(duration)

    return {
        "ts_start": current_time, "ts_end": finish_time
    }