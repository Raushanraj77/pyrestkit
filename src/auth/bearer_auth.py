from src.auth.auth_strategy import AuthenticationStrategy


class BearerAuth(AuthenticationStrategy):
    """Bearer token authentication."""

    def __init__(self, token: str) -> None:
        self._token = token

    def get_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token}",
        }
