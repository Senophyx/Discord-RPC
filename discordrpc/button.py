from dataclasses import dataclass

from discordrpc import InvalidURL


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
            self.payload = [i.get_payload() for i in args[0] if isinstance(i, Button)]
        else:
            self.payload = [i.get_payload() for i in args if isinstance(i, Button)]

    def get_payloads(self):
        return self.payload
