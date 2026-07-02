from requests import Response


class ResponseValidator:

    def __init__(self, response: Response):
        self.response = response

    def status_code(self, expected: int) -> "ResponseValidator":
        assert self.response.status_code == expected
        return self

    def has_key(self, key: str) -> "ResponseValidator":
        assert key in self.response.json()
        return self

    def field_equals(
        self,
        key: str,
        value,
    ) -> "ResponseValidator":

        assert self.response.json()[key] == value
        return self