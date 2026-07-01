from __future__ import annotations

from typing import Any

from requests import Response

from src.core.api_client import APIClient
from src.endpoints.user_endpoints import UserEndpoints


class UserClient:
    """
    Business client for User APIs.

    This class contains only business operations.
    It delegates all HTTP communication to APIClient.
    """

    def __init__(self, api_client: APIClient) -> None:
        self._api_client = api_client

    def list_users(self, **kwargs: Any) -> Response:
        return self._api_client.get(
            UserEndpoints.list_users(),
            **kwargs,
        )

    def get_user(
        self,
        user_id: int,
        **kwargs: Any,
    ) -> Response:
        return self._api_client.get(
            UserEndpoints.get_user(user_id=user_id),
            **kwargs,
        )

    def create_user(
        self,
        payload: dict[str, Any],
        **kwargs: Any,
    ) -> Response:
        return self._api_client.post(
            UserEndpoints.create_user(),
            json=payload,
            **kwargs,
        )

    def update_user(
        self,
        user_id: int,
        payload: dict[str, Any],
        **kwargs: Any,
    ) -> Response:
        return self._api_client.put(
            UserEndpoints.update_user(user_id=user_id),
            json=payload,
            **kwargs,
        )

    def delete_user(
        self,
        user_id: int,
        **kwargs: Any,
    ) -> Response:
        return self._api_client.delete(
            UserEndpoints.delete_user(user_id=user_id),
            **kwargs,
        )