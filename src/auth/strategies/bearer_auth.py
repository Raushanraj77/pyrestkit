from src.auth.auth_strategy import AuthenticationStrategy
from src.auth.token_manager import TokenManager


class BearerAuth(AuthenticationStrategy):
    def __init__(
        self,
        token_manager: TokenManager,
    ) -> None:
        self._token_manager = token_manager

    def get_headers(self) -> dict[str, str]:
        token = self._token_manager.get_token()

        return {
            "Authorization": f"Bearer {token}",
        }
