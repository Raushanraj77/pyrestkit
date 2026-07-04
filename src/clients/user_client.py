from __future__ import annotations

from dataclasses import asdict

from src.clients.base_client import BaseClient
from src.core.api_client import APIClient
from src.endpoints.user_endpoints import UserEndpoints
from src.models.request.create_user_request import CreateUserRequest
from src.models.request.update_user_request import UpdateUserRequest
from src.response.framework_response import FrameworkResponse


class UserClient(BaseClient):
    """
    Business client responsible for User APIs.

    This client delegates HTTP operations to BaseClient.
    """

    def __init__(
        self,
        api_client: APIClient,
    ) -> None:
        super().__init__(api_client)

    def list_users(
        self,
    ) -> FrameworkResponse:
        return self.get(
            UserEndpoints.list_users(),
        )

    def get_user(
        self,
        user_id: int,
    ) -> FrameworkResponse:
        return self.get(
            UserEndpoints.get_user(user_id),
        )

    def create_user(
        self,
        request: CreateUserRequest,
    ) -> FrameworkResponse:
        return self.post(
            UserEndpoints.create_user(),
            json=asdict(request),
        )

    def update_user(
        self,
        user_id: int,
        request: UpdateUserRequest,
    ) -> FrameworkResponse:
        return self.put(
            UserEndpoints.update_user(user_id),
            json=asdict(request),
        )

    def delete_user(
        self,
        user_id: int,
    ) -> FrameworkResponse:
        return self.delete(
            UserEndpoints.delete_user(user_id),
        )
