import sys

class LanciumError(Exception):
    """Base class for all exceptions"""
    def __init__(self, message=None):
        sys.tracebacklimit=0
        self.message=message

    def __str__(self):
        if self.message:
            return f"{self.message}"


class InternalError(LanciumError):
    pass


class ResourceNotFoundError(LanciumError):
    pass


class InvalidInputError(LanciumError):
    pass


class DeprecatedAPIError(LanciumError):
    pass

class InvalidByteRangeError(LanciumError):
    pass

class PathIsDirectoryError(LanciumError):
    pass

class ForbiddenDataError(LanciumError):
    pass

class UnavailableDataError(LanciumError):
    pass

class BadDataRequestError(LanciumError):
    sys.tracebacklimit=0
    def __init__(self, id=None, message=None):
        self.id = id
        self.message = message

class DataConflictError(LanciumError):
    pass
