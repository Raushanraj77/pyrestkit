from pyrestkit.auth.token_cache import TokenCache
from pyrestkit.auth.token_response import TokenResponse


def test_cache_set_and_get() -> None:
    cache = TokenCache()

    response = TokenResponse(
        access_token="abc123",
        expires_in=3600,
    )

    cache.set(response)

    token = cache.get()

    assert token is not None
    assert token.access_token == "abc123"
