from __future__ import annotations

from typing import TYPE_CHECKING

from pyrestkit.assertions.assertion_exception import AssertionException
from pyrestkit.validators.schema_validator import SchemaValidator

if TYPE_CHECKING:
    from pyrestkit.response.framework_response import FrameworkResponse


class ResponseAssertions:
    """
    Fluent assertions for FrameworkResponse.
    """

    def __init__(
        self,
        response: FrameworkResponse,
    ) -> None:
        self._response = response

    def have_status(
        self,
        expected: int,
    ) -> ResponseAssertions:
        actual = self._response.status_code

        if actual != expected:
            raise AssertionException(
                f"Expected status code {expected}, but received {actual}."
            )

        return self

    def be_successful(
        self,
    ) -> ResponseAssertions:
        if not self._response.ok:
            raise AssertionException(
                f"Expected successful response "
                f"but received {self._response.status_code}."
            )

        return self

    def have_header(
        self,
        name: str,
        expected: str | None = None,
    ) -> ResponseAssertions:
        headers = self._response.headers

        if name not in headers:
            raise AssertionException(f"Header '{name}' was not found.")

        if expected is not None:
            actual = headers[name]

            if actual != expected:
                raise AssertionException(
                    f"Expected header '{name}' to be '{expected}', but was '{actual}'."
                )

        return self

    def match_schema(
        self,
        schema_path: str,
    ) -> ResponseAssertions:
        SchemaValidator.validate(
            self._response,
            schema_path,
        )

        return self

    def _get_json_value(
        self,
        path: str,
    ) -> object:
        """
        Returns a nested JSON value using dot notation.

        Example:

            data.email
            support.url
        """

        value: object = self._response.json()

        for part in path.split("."):
            if not isinstance(value, dict):
                raise AssertionException(f"'{path}' does not exist.")

            if part not in value:
                raise AssertionException(f"Key '{part}' not found in '{path}'.")

            value = value[part]

        return value

    def have_json(
        self,
        path: str,
        expected: object,
    ) -> ResponseAssertions:
        actual = self._get_json_value(path)

        if actual != expected:
            raise AssertionException(
                f"Expected '{path}' to be {expected!r}, but was {actual!r}."
            )

        return self

    def respond_within(
        self,
        milliseconds: int,
    ) -> ResponseAssertions:
        """
        Verifies that the response completed within the
        specified number of milliseconds.
        """

        actual = self._response.elapsed.total_seconds() * 1000

        if actual > milliseconds:
            raise AssertionException(
                f"Expected response within {milliseconds} ms, but took {actual:.2f} ms."
            )

        return self

    def have_json_count(
        self,
        path: str,
        expected: int,
    ) -> ResponseAssertions:
        """
        Verifies the number of items
        in a JSON array.
        """

        value = self._response.body.get(path)

        if not isinstance(
            value,
            list,
        ):
            raise AssertionException(f"'{path}' is not a JSON array.")

        actual = len(value)

        if actual != expected:
            raise AssertionException(
                f"Expected {expected} items at '{path}', but found {actual}."
            )

        return self

    def have_json_contains(
        self,
        path: str,
        expected: object,
    ) -> ResponseAssertions:
        """
        Verifies that a JSON array contains
        the expected value.
        """

        value = self._response.body.get(path)

        if not isinstance(value, list):
            raise AssertionException(f"'{path}' is not a JSON array.")

        if expected not in value:
            raise AssertionException(f"{expected!r} not found in '{path}'.")

        return self
