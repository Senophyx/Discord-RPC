from .exceptions import *

valid_url = ["https://", "http://"]

def button_one(label:str, url:str):
    if any(v in url for v in valid_url):
        payloads = {"label": label, "url": url}
        return payloads
    else:
        raise InvalidURL

def button_two(label:str, url:str):
    if any(v in url for v in valid_url):
        payloads = {"label": label, "url": url}
        return payloads
    else:
        raise InvalidURL

def button(
    button_one_label:str=None,
    button_two_label:str=None,
    button_one_url:str=None,
    button_two_url:str=None):
    
    if button_one_label == None:
        raise ButtonError('"button_one_label" cannot None')
    if button_one_url == None:
        raise ButtonError('"button_one_url" cannot None')
    if button_two_label == None:
        raise ButtonError('"button_two_label" cannot None')
    if button_two_url == None:
        raise ButtonError('"button_two_url" cannot None')
    
    btn_one = button_one(label=button_one_label, url=button_one_url)
    btn_two = button_two(label=button_two_label, url=button_two_url)
    payloads = [btn_one, btn_two]

    return payloads
