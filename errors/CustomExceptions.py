class PatriotError(Exception):
    def __init__(self, message):
        if message is None or message == "":
            self.message = "Unfortunately, an error occurred"
        else:
            self.message = message

        super(PatriotError, self).__init__(self.message)


class AccessViolationError(PatriotError):
    def __init__(self, message):
        super(AccessViolationError, self).__init__(message)


class CommandProcessingError(PatriotError):
    def __init__(self, message):
        super(CommandProcessingError, self).__init__(message)


class CommandNotFoundError(PatriotError):
    def __init__(self, message):
        super(CommandNotFoundError, self).__init__(message)


class InitializationError(PatriotError):
    def __init__(self, message):
        super(InitializationError, self).__init__(message)
