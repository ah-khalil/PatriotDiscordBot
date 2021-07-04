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


class ConfigIOError(PatriotError):
    def __init__(self, message):
        super(ConfigIOError, self).__init__(message)


class ConfigError(PatriotError):
    def __init__(self, message):
        super(ConfigError, self).__init__(message)


class APIError(PatriotError):
    def __init__(self, message):
        super(APIError, self).__init__(message)


class NoSearchResultError(PatriotError):
    def __init__(self, message):
        super(NoSearchResultError, self).__init__(message)


class ConfigurationError(PatriotError):
    def __init__(self, message):
        super(ConfigurationError, self).__init__(message)