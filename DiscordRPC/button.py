valid_url = ["https://", "http://"]

def button_one(label:str, url:str):
    if any(v in url for v in valid_url):
        payloads = {"label": label, "url": url}
        return payloads
    else:
        raise TypeError("Invalid URL. Must include: http:// or https://")

def button_two(label:str, url:str):
    if any(v in url for v in valid_url):
        payloads = {"label": label, "url": url}
        return payloads
    else:
        raise TypeError("Invalid URL. Must include: http:// or https://")

def button(button_one_label:str, button_two_label:str, button_one_url:str, button_two_url:str):
    btn_one = button_one(label=button_one_label, url=button_one_url)
    btn_two = button_two(label=button_two_label, url=button_two_url)
    payloads = [btn_one, btn_two]

    return payloads
