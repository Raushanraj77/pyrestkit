from pyrestkit.exceptions.api_exception import APIException


class NetworkException(APIException):
    """
    Raised for network related failures.
    """

    def __init__(self, message: str = "Network error occurred.") -> None:
        super().__init__(message)
