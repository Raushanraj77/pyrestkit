from src.auth.authentication_manager import AuthenticationManager
from src.auth.bearer_auth import BearerAuth


def test_authentication_manager_returns_headers() -> None:
    manager = AuthenticationManager(BearerAuth("token123"))

    headers = manager.get_headers()

    assert headers == {
        "Authorization": "Bearer token123",
    }


def test_authentication_manager_without_strategy() -> None:
    manager = AuthenticationManager()

    assert manager.get_headers() == {}
