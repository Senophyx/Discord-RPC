from dataclasses import dataclass

from discordrpc import InvalidURL, ButtonError


@dataclass
class Button:
    label: str
    url: str

    def get_payload(self):
        if not any(v in self.url for v in ["https://", "http://"]):
            raise InvalidURL
        return {"label": self.label, "url": self.url}


class Buttons:
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], list):
            payload = [i.get_payload() for i in args[0] if isinstance(i, Button)]
        else:
            payload = [i.get_payload() for i in args if isinstance(i, Button)]

        count_buttons = len(payload)
        if count_buttons == 0 or count_buttons > 2:
            raise ButtonError("The number of buttons exceeds two or there are none at all")
        
        self.payload = payload

    def get_payloads(self):
        return self.payload
