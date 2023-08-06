from lancium.errors.common import LanciumError

class DirectoryNotEmptyError(LanciumError):
    pass

class NoContentError(LanciumError):
    pass

class PartialContentError(LanciumError):
    pass