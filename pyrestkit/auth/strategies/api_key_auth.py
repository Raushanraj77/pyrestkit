from pyrestkit.auth.auth_strategy import AuthenticationStrategy


class ApiKeyAuth(AuthenticationStrategy):
    """API Key Authentication."""

    def __init__(
        self,
        api_key: str,
        header_name: str = "x-api-key",
    ) -> None:
        self._api_key = api_key
        self._header_name = header_name

    def get_headers(self) -> dict[str, str]:
        return {
            self._header_name: self._api_key,
        }
