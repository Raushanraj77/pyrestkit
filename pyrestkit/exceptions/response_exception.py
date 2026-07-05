from pyrestkit.exceptions.api_exception import APIException


class ResponseException(APIException):
    """
    Raised for unexpected HTTP responses.
    """

    def __init__(self, message: str = "Unexpected response received.") -> None:
        super().__init__(message)
