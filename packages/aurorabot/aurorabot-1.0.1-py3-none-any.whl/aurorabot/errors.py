class AuroraBotException(Exception):
    pass

class MissingDeviceAuth(AuroraBotException):
    pass

class CommandNotFound(Exception):
    pass