from src.auth.authentication_manager import AuthenticationManager
from src.auth.bearer_auth import BearerAuth
from src.auth.token_manager import TokenManager


def test_authentication_manager_returns_headers(
    token_manager: TokenManager,
) -> None:
    auth = BearerAuth(token_manager)
    manager = AuthenticationManager(auth)

    assert manager.get_headers() == {
        "Authorization": "Bearer fake-token",
    }


def test_authentication_manager_without_strategy() -> None:
    manager = AuthenticationManager()

    assert manager.get_headers() == {}
