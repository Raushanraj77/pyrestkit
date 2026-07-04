import base64

from pyrestkit.auth.auth_strategy import AuthenticationStrategy


class BasicAuth(AuthenticationStrategy):
    """HTTP Basic Authentication."""

    def __init__(
        self,
        username: str,
        password: str,
    ) -> None:
        self._username = username
        self._password = password

    def get_headers(self) -> dict[str, str]:
        credentials = (f"{self._username}:{self._password}").encode()

        encoded = base64.b64encode(credentials).decode("utf-8")

        return {
            "Authorization": f"Basic {encoded}",
        }
