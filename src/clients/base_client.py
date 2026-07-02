from __future__ import annotations

from typing import Any

from requests import Response

from src.core.api_client import APIClient


class BaseClient:
    """
    Base class for all business clients.
    """

    def __init__(self, api_client: APIClient) -> None:
        self._api_client = api_client

    def get(
        self,
        endpoint: str,
        **kwargs: Any,
    ) -> Response:
        return self._api_client.get(endpoint, **kwargs)

    def post(
        self,
        endpoint: str,
        **kwargs: Any,
    ) -> Response:
        return self._api_client.post(endpoint, **kwargs)

    def put(
        self,
        endpoint: str,
        **kwargs: Any,
    ) -> Response:
        return self._api_client.put(endpoint, **kwargs)

    def patch(
        self,
        endpoint: str,
        **kwargs: Any,
    ) -> Response:
        return self._api_client.patch(endpoint, **kwargs)

    def delete(
        self,
        endpoint: str,
        **kwargs: Any,
    ) -> Response:
        return self._api_client.delete(endpoint, **kwargs)
