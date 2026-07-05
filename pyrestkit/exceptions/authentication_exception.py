from pyrestkit.exceptions.api_exception import APIException


class AuthenticationException(APIException):
    """
    Raised when authentication fails.
    """

    def __init__(self, message: str = "Authentication failed.") -> None:
        super().__init__(message)
