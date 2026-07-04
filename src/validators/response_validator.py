from typing import Any

from requests import Response

from src.exceptions.validation_exception import ValidationException


class ResponseValidator:
    def __init__(self, response: Response):
        self.response = response

    def status_code(self, expected: int) -> "ResponseValidator":
        assert self.response.status_code == expected

        if self.response.status_code != expected:
            raise ValidationException(
                f"Expected status {expected}, received {self.response.status_code}"
            )

        return self

    def has_key(self, key: str) -> "ResponseValidator":
        assert key in self.response.json()
        return self

    def field_equals(
        self,
        key: str,
        value: Any,
    ) -> "ResponseValidator":
        assert self.response.json()[key] == value
        return self
