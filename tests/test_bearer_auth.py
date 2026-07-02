from src.auth.bearer_auth import BearerAuth
from src.auth.token_manager import TokenManager
from tests.fake_token_provider import FakeTokenProvider


def test_bearer_auth_headers() -> None:
    provider = FakeTokenProvider()

    manager = TokenManager(provider)

    auth = BearerAuth(manager)

    assert auth.get_headers() == {
        "Authorization": "Bearer fake-token",
    }
