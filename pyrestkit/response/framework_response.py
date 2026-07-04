from __future__ import annotations

from collections.abc import Mapping
from dataclasses import is_dataclass
from datetime import timedelta
from typing import TYPE_CHECKING, Any, TypeVar

import requests

from pyrestkit.response.response_body import ResponseBody

if TYPE_CHECKING:
    from pyrestkit.assertions.response_assertions import ResponseAssertions

T = TypeVar("T")


class FrameworkResponse:
    """
    Wrapper around requests.Response.

    Adds framework features while still exposing
    the original response.
    """

    def __init__(
        self,
        response: requests.Response,
    ) -> None:
        self._response = response
        self._body: ResponseBody | None = None

    @property
    def raw(
        self,
    ) -> requests.Response:
        return self._response

    @property
    def should(
        self,
    ) -> ResponseAssertions:
        from pyrestkit.assertions.response_assertions import (
            ResponseAssertions,
        )

        return ResponseAssertions(self)

    @property
    def status(
        self,
    ) -> int:
        return self._response.status_code

    @property
    def status_code(
        self,
    ) -> int:
        return self._response.status_code

    @property
    def headers(
        self,
    ) -> Mapping[str, str]:
        return self._response.headers

    @property
    def text(
        self,
    ) -> str:
        return self._response.text

    @property
    def elapsed(
        self,
    ) -> timedelta:
        return self._response.elapsed

    @property
    def body(
        self,
    ) -> ResponseBody:
        if self._body is None:
            self._body = ResponseBody(
                self._response.json(),
            )

        return self._body

    def json(
        self,
    ) -> Any:
        return self._response.json()

    def as_model(
        self,
        model: type[T],
        path: str | None = None,
    ) -> T:
        """
        Deserialize a JSON object into a dataclass.

        Examples:

            response.as_model(User)

            response.as_model(User, path="data")

            response.as_model(User, path="result.user")
        """
        if not is_dataclass(model):
            raise TypeError(
                f"{model.__name__} is not a dataclass.",
            )

        data = self._get_value(path)

        if not isinstance(data, dict):
            raise TypeError(
                "Expected a JSON object.",
            )

        return model(**data)

    def _get_value(
        self,
        path: str | None = None,
    ) -> Any:
        """
        Returns a value from the response JSON using dot notation.

        Examples:

            None
                -> whole JSON

            "data"
                -> json()["data"]

            "data.user"
                -> json()["data"]["user"]
        """
        data = self.json()

        if path is None:
            return data

        for key in path.split("."):
            if not isinstance(data, dict):
                raise TypeError(
                    f"Cannot access '{key}' as the current value is not a JSON object.",
                )

            if key not in data:
                raise KeyError(
                    f"Path '{path}' not found in response.",
                )

            data = data[key]

        return data

    def as_list(
        self,
        model: type[T],
        path: str | None = None,
    ) -> list[T]:
        """
        Deserialize a JSON array into a list of dataclasses.

        Examples:

            response.as_list(User)

            response.as_list(User, path="data")

            response.as_list(User, path="result.users")
        """
        if not is_dataclass(model):
            raise TypeError(
                f"{model.__name__} is not a dataclass.",
            )

        data = self._get_value(path)

        if not isinstance(data, list):
            raise TypeError(
                "Expected a JSON array.",
            )

        return [model(**item) for item in data]

    def raise_for_status(
        self,
    ) -> None:
        self._response.raise_for_status()

    def __getattr__(
        self,
        name: str,
    ) -> Any:
        """
        Delegate unknown attributes to requests.Response.
        """
        return getattr(
            self._response,
            name,
        )

    def __repr__(
        self,
    ) -> str:
        return repr(self._response)

    def __str__(
        self,
    ) -> str:
        return str(self._response)
