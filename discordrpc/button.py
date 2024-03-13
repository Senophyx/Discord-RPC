from .exceptions import *

valid_url = ["https://", "http://"]

def _payload(label:str, url:str):
    if any(v in url for v in valid_url):
        payloads = {"label": label, "url": url}
        return payloads
    else:
        raise InvalidURL
    

def Button(
    button_one_label:str,
    button_one_url:str,
    button_two_label:str,
    button_two_url:str):
    
    if button_one_label == None:
        raise ButtonError('"button_one_label" cannot None')
    if button_one_url == None:
        raise ButtonError('"button_one_url" cannot None')
    if button_two_label == None:
        raise ButtonError('"button_two_label" cannot None')
    if button_two_url == None:
        raise ButtonError('"button_two_url" cannot None')
    
    btn_one = _payload(label=button_one_label, url=button_one_url)
    btn_two = _payload(label=button_two_label, url=button_two_url)
    payloads = [btn_one, btn_two]

    return payloads