from .exceptions import InvalidURL
from .utils import valid_url


def button(text:str, url:str):
    return {"label": text, "url": valid_url(url)}
