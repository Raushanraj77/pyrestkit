from __future__ import annotations

from typing import Any

from requests import Response

from pyrestkit.exceptions.validation_exception import ValidationException


class ResponseValidator:
    def __init__(self, response: Response) -> None:
        self.response = response

    def status_code(self, expected: int) -> ResponseValidator:
        if self.response.status_code != expected:
            raise ValidationException(
                "Expected status code "
                f"{expected}, received {self.response.status_code}."
            )

        return self

    def has_key(self, key: str) -> ResponseValidator:
        payload = self._json_payload()

        if key not in payload:
            raise ValidationException(f"Response does not contain key '{key}'.")

        return self

    def field_equals(
        self,
        key: str,
        value: Any,
    ) -> ResponseValidator:
        payload = self._json_payload()

        if key not in payload:
            raise ValidationException(f"Response does not contain key '{key}'.")

        if payload[key] != value:
            raise ValidationException(
                f"Response field '{key}' expected {value!r}, received {payload[key]!r}."
            )

        return self

    def _json_payload(self) -> dict[str, Any]:
        try:
            payload = self.response.json()
        except ValueError as exc:
            raise ValidationException("Response body is not valid JSON.") from exc

        if not isinstance(payload, dict):
            raise ValidationException("Response body must be a JSON object.")

        return payload
