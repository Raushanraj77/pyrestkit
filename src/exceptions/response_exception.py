from src.exceptions.api_exception import APIException


class ResponseException(APIException):
    """
    Raised for unexpected HTTP responses.
    """

    pass
