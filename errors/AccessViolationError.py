class AccessViolationError(Exception):
    def __init__(self, message):
        super(AccessViolationError, self).__init__(message)