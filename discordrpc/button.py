from .utils import required_url


def button(text: str, url: str):
    return {"label": text, "url": required_url(url)}
