class CommandNotFoundError(Exception):
    def __init__(self, message=""):
        super(CommandNotFoundError, self).__init__(message)