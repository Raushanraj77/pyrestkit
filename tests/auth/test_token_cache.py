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


def test_cache_returns_none_when_expired_or_unset() -> None:
    cache = TokenCache()

    assert cache.get() is None

    expired = TokenResponse(access_token="expired", expires_in=-1)
    cache.set(expired)

    assert cache.get() is None


def test_cache_clear_removes_cached_response() -> None:
    cache = TokenCache()
    cache.set(TokenResponse(access_token="abc123", expires_in=3600))

    cache.clear()

    assert cache.get() is None
