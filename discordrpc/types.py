from enum import Enum


# https://discord.com/developers/docs/events/gateway-events#activity-object-activity-types
# Activity Type 1 and 4 currently disabled. See https://github.com/Senophyx/Discord-RPC/issues/28#issuecomment-2301287350

class Activity(Enum):
    Playing = 0
    #Streaming = 1
    Listening = 2
    Watching = 3
    #Custom = 4
    Competing = 5
