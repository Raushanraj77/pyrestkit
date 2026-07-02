from dataclasses import asdict

from requests import Response

from src.core.api_client import APIClient
from src.endpoints.user_endpoints import UserEndpoints
from src.models.request.create_user_request import CreateUserRequest
from src.models.request.update_user_request import UpdateUserRequest


class UserClient:

    def __init__(self, api_client: APIClient):
        self._api_client = api_client

    def list_users(self) -> Response:
        return self._api_client.get(
            UserEndpoints.list_users()
        )

    def get_user(
        self,
        user_id: int,
    ) -> Response:
        return self._api_client.get(
            UserEndpoints.get_user(user_id)
        )

    def create_user(
        self,
        request: CreateUserRequest,
    ) -> Response:

        return self._api_client.post(
            UserEndpoints.create_user(),
            json=asdict(request)
        )

    def update_user(
        self,
        user_id: int,
        request: UpdateUserRequest,
    ) -> Response:

        return self._api_client.put(
            UserEndpoints.update_user(user_id),
            json=asdict(request)
        )

    def delete_user(
        self,
        user_id: int,
    ) -> Response:

        return self._api_client.delete(
            UserEndpoints.delete_user(user_id)
        )