from .exceptions import *


def Button(text:str, url:str):
    if not url.startswith(("http://", "https://")):
        raise InvalidURL()
    return {"label": text, "url": url}
