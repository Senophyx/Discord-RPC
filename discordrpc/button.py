from dataclasses import dataclass

from discordrpc import InvalidURL, ButtonError


@dataclass
class _Button:
    label: str
    url: str

    def get_payload(self):
        if not any(v in self.url for v in ["https://", "http://"]):
            raise InvalidURL
        return {"label": self.label, "url": self.url}


def Button(
        button_one_label: str,
        button_one_url: str,
        button_two_label: str,
        button_two_url: str):
    for button in [button_one_label, button_two_label, button_one_url, button_two_url]:
        if button is None:
            raise ButtonError('"button" cannot None')

    payloads = [
        _Button(label=button_one_label, url=button_one_url).get_payload(),
        _Button(label=button_two_label, url=button_two_url).get_payload()
    ]

    return payloads

