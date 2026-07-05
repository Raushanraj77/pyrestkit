from pyrestkit.exceptions.api_exception import APIException


class ConfigurationException(APIException):
    """
    Raised when configuration is invalid.
    """

    def __init__(self, message: str = "Configuration is invalid.") -> None:
        super().__init__(message)
