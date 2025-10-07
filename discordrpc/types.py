from enum import Enum


# https://discord.com/developers/docs/events/gateway-events#activity-object-activity-types
class Activity(Enum):
    Playing = 0
    Streaming = 1
    Listening = 2
    Watching = 3
    Custom = 4
    Competing = 5


class User():
    def __init__(self, data:dict=None):
        data = data or {}
        self.id: int = int(data.get('id', 0))
        self.username: str = data.get('username')
        self.name: str = data.get('global_name')
        self.avatar: str = self._parse_avatar(data)
        self.bot: bool = data.get('bot', False)
        self.premium_type: int = int(data.get('premium_type', 0)) # https://discord.com/developers/docs/resources/user#user-object-premium-types

    def _parse_avatar(self, data:dict, size:int=1024) -> str:
        if data.get('avatar'):
            ext = "gif" if data.get('avatar').startswith("a_") else "png"
            return f"https://cdn.discordapp.com/avatars/{self.id}/{data.get('avatar')}.{ext}?size={size}"
        else:
            return f"https://cdn.discordapp.com/embed/avatars/0.png"

    def __str__(self):
        return f"User({self.name})"
