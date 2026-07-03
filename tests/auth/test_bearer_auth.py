from src.auth.strategies.bearer_auth import BearerAuth
from src.auth.token_cache import TokenCache
from src.auth.token_manager import TokenManager
from src.auth.token_response import TokenResponse
from tests.fake_token_provider import FakeTokenProvider


def test_bearer_auth_headers() -> None:
    provider = FakeTokenProvider()

    cache = TokenCache()
    cache.set(
        TokenResponse(
            access_token="fake-token",
            expires_in=3600,
        )
    )

    manager = TokenManager(provider, cache)

    auth = BearerAuth(manager)

    assert auth.get_headers() == {
        "Authorization": "Bearer fake-token",
    }

    assert provider.call_count == 0
