class ForbiddenError(Exception):
    """AuthedUser does not have allowable role"""

    pass


class MissingAuthHeaderError(Exception):
    """HTTP Request does not have an Authorization Header value"""

    pass


class InvalidAuthHeaderValueError(Exception):
    """HTTP Request does not have valid Authorization Header value for JWT"""

    pass


class UnsupportedJwtAlgError(Exception):
    """Algorithm specified for JWT Service is Unsupported"""

    pass


class JWTDecodeError(Exception):
    """Algorithm specified for JWT Service is Unsupported"""

    pass
