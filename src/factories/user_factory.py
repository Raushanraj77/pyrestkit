from __future__ import annotations

import random

from src.factories.base_factory import BaseFactory
from src.models.request.create_user_request import CreateUserRequest


class UserFactory(BaseFactory):
    """
    Factory for CreateUserRequest objects.
    """

    @classmethod
    def random(cls) -> CreateUserRequest:
        return CreateUserRequest(
            name=f"User-{random.randint(1000, 9999)}",
            job="QA Engineer",
        )

    @classmethod
    def admin(cls) -> CreateUserRequest:
        return CreateUserRequest(
            name="Admin User",
            job="Administrator",
        )

    @classmethod
    def from_file(
        cls,
        filename: str,
    ) -> CreateUserRequest:
        data = cls.load_json(filename)

        return CreateUserRequest(
            **data,
        )
