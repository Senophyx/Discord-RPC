class RPCException(Exception):
    def __init__(self, message: str= None):
        if message is None:
            message = 'An error has occurred within DiscordRPC'
        super().__init__(message)

class Error(RPCException):
    def __init__(self, message:str):
        super().__init__(message)

class DiscordNotOpened(RPCException):
    def __init__(self):
        super().__init__("Error, could not find Discord. is Discord running?")

class ActivityError(RPCException):
    def __init__(self):
        super().__init__("An error has occurred in activity payload, do you have set your activity correctly?")

class InvalidURL(RPCException):
    def __init__(self):
        super().__init__("Invalid URL. Must include: http:// or https://")

class InvalidID(RPCException):
    def __init__(self):
        super().__init__("Invalid ID, is the ID correct? Get Application ID on https://discord.com/developers/applications")

class ButtonError(RPCException):
    def __init__(self, message: str = None):
        super().__init__(message=message)

class ProgressbarError(RPCException):
    def __init__(self, message):
        super().__init__(message=message)

class InvalidActivityType(RPCException):
    def __init__(self, message):
        super().__init__(f"Activity type must be <Activity>, not {message}")

# https://github.com/Senophyx/Discord-RPC/issues/28#issuecomment-2301287350
class ActivityTypeDisabled(RPCException):
    def __init__(self):
        super().__init__(f"Activity Type 1 and 4 currently disabled. See https://github.com/Senophyx/Discord-RPC/issues/28#issuecomment-2301287350")
