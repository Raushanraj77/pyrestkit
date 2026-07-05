class APIException(Exception):
    """
    Base exception for the API automation framework.
    """

    def __init__(self, message: str = "") -> None:
        super().__init__(message)
        self.message = message
