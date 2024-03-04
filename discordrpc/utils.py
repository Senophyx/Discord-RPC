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