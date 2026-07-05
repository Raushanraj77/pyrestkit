from pyrestkit.exceptions.api_exception import APIException


class SerializationException(APIException):
    """
    Raised when serialization/deserialization fails.
    """

    def __init__(self, message: str = "Serialization failed.") -> None:
        super().__init__(message)
