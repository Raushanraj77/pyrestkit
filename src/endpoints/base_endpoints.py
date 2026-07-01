"""
Base endpoint definitions.

All endpoint classes should inherit from this class.
"""


class BaseEndpoints:
    """
    Base class responsible for building API endpoint paths.

    Future enhancements:
    - API versioning
    - Service prefixes
    - Tenant support
    """

    API_VERSION = ""

    @classmethod
    def build(cls, path: str) -> str:
        """
        Returns complete endpoint path.

        Example:
            "/users"

        Future:
            "/api/v1/users"
        """

        return f"{cls.API_VERSION}{path}"