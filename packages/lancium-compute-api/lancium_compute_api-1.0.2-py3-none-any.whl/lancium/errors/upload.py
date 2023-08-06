from lancium.errors.common import LanciumError


class FileCompleteConflict(LanciumError):
    pass


class FileChecksumMismatch(LanciumError):
    pass


class MissingContentLength(LanciumError):
    pass


class FileUploadError(LanciumError):
    pass
