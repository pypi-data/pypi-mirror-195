from lancium.errors.common import LanciumError


class MissingCredentialsError(LanciumError):
    pass


class InvalidCredentialsError(LanciumError):
    pass
