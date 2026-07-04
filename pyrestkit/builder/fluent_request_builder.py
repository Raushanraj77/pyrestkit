from __future__ import annotations

from typing import Any

from pyrestkit.core.api_client import APIClient
from pyrestkit.response.framework_response import FrameworkResponse


class FluentRequestBuilder:
    """
    Fluent API for building and sending HTTP requests.

    Example:

        response = (
            api.request()
            .get("/users")
            .query(page=2)
            .header("Authorization", token)
            .send()
        )
    """

    def __init__(
        self,
        client: APIClient,
    ) -> None:
        self._client = client

        self._method = ""
        self._endpoint = ""

        self._kwargs: dict[str, Any] = {}

    def get(
        self,
        endpoint: str,
    ) -> FluentRequestBuilder:
        self._method = "GET"
        self._endpoint = endpoint
        return self

    def post(
        self,
        endpoint: str,
    ) -> FluentRequestBuilder:
        self._method = "POST"
        self._endpoint = endpoint
        return self

    def put(
        self,
        endpoint: str,
    ) -> FluentRequestBuilder:
        self._method = "PUT"
        self._endpoint = endpoint
        return self

    def patch(
        self,
        endpoint: str,
    ) -> FluentRequestBuilder:
        self._method = "PATCH"
        self._endpoint = endpoint
        return self

    def delete(
        self,
        endpoint: str,
    ) -> FluentRequestBuilder:
        self._method = "DELETE"
        self._endpoint = endpoint
        return self

    def query(
        self,
        **params: Any,
    ) -> FluentRequestBuilder:
        self._kwargs["params"] = params
        return self

    def header(
        self,
        name: str,
        value: str,
    ) -> FluentRequestBuilder:
        headers = self._kwargs.setdefault(
            "headers",
            {},
        )

        headers[name] = value

        return self

    def headers(
        self,
        headers: dict[str, str],
    ) -> FluentRequestBuilder:
        current = self._kwargs.setdefault(
            "headers",
            {},
        )

        current.update(headers)

        return self

    def json(
        self,
        body: Any,
    ) -> FluentRequestBuilder:
        self._kwargs["json"] = body
        return self

    def data(
        self,
        body: Any,
    ) -> FluentRequestBuilder:
        self._kwargs["data"] = body
        return self

    def timeout(
        self,
        seconds: int,
    ) -> FluentRequestBuilder:
        self._kwargs["timeout"] = seconds
        return self

    def send(
        self,
    ) -> FrameworkResponse:
        method = self._method.upper()

        if method == "GET":
            return self._client.get(
                self._endpoint,
                **self._kwargs,
            )

        if method == "POST":
            return self._client.post(
                self._endpoint,
                **self._kwargs,
            )

        if method == "PUT":
            return self._client.put(
                self._endpoint,
                **self._kwargs,
            )

        if method == "PATCH":
            return self._client.patch(
                self._endpoint,
                **self._kwargs,
            )

        if method == "DELETE":
            return self._client.delete(
                self._endpoint,
                **self._kwargs,
            )

        raise ValueError(
            "HTTP method not selected.",
        )
