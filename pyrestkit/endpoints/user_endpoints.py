"""
User endpoint definitions.
"""

from pyrestkit.endpoints.base_endpoints import BaseEndpoints


class UserEndpoints(BaseEndpoints):
    """
    Contains all endpoints related to Users.
    """

    RESOURCE = "/users"

    @classmethod
    def list_users(cls) -> str:
        """
        GET /users
        """
        return cls.build(cls.RESOURCE)

    @classmethod
    def create_user(cls) -> str:
        """
        POST /users
        """
        return cls.build(cls.RESOURCE)

    @classmethod
    def get_user(cls, user_id: int) -> str:
        """
        GET /users/{id}
        """
        return cls.build(f"{cls.RESOURCE}/{user_id}")

    @classmethod
    def update_user(cls, user_id: int) -> str:
        """
        PUT /users/{id}
        """
        return cls.build(f"{cls.RESOURCE}/{user_id}")

    @classmethod
    def delete_user(cls, user_id: int) -> str:
        """
        DELETE /users/{id}
        """
        return cls.build(f"{cls.RESOURCE}/{user_id}")
