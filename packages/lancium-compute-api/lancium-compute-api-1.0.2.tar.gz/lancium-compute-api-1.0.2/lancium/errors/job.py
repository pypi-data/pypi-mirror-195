from lancium.errors.common import LanciumError
import sys


class JobValidationError(LanciumError):
    sys.tracebacklimit=0
    def __init__(self, id=None, message=None):
        self.id = id
        self.message = message

class JobTerminationError(LanciumError):
    pass

class BillingInfoError(LanciumError):
    pass


class QoSUnavailableError(LanciumError):
    pass


class InvalidInputTypeError(LanciumError):
    pass


class JobAlreadySubmittedError(LanciumError):
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

class JobNotRunningError(LanciumError):
    pass
