from pyrestkit.exceptions.api_exception import APIException


class ValidationException(APIException):
    """
    Raised when response validation fails.
    """

    def __init__(self, message: str = "Validation failed.") -> None:
        super().__init__(message)
