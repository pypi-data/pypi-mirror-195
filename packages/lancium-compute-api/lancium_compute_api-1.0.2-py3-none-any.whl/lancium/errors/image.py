from lancium.errors.common import LanciumError
import sys


class ImageValidationError(LanciumError):
    sys.tracebacklimit=0
    def __init__(self, name=None, message=None):
        self.name = name
        self.message = message


class ImageRebuildError(LanciumError):
    pass

class ForbiddenNamespaceError(LanciumError):
    pass
