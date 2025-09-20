from enum import Enum


# https://discord.com/developers/docs/events/gateway-events#activity-object-activity-types

class Activity(Enum):
    Playing = 0
    Streaming = 1
    Listening = 2
    Watching = 3
    Custom = 4
    Competing = 5

class StatusDisplay(Enum):
    Name = 0
    State = 1
    Details = 2