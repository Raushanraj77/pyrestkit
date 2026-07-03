from src.auth.token_cache import TokenCache
from src.auth.token_manager import TokenManager
from tests.fake_token_provider import FakeTokenProvider


def test_token_cached() -> None:
    provider = FakeTokenProvider()

    cache = TokenCache()

    manager = TokenManager(
        provider=provider,
        cache=cache,
    )

    token1 = manager.get_token()
    token2 = manager.get_token()

    assert token1 == "fake-token"
    assert token2 == "fake-token"

    assert provider.call_count == 1
