from src.auth.token_manager import TokenManager
from tests.fake_token_provider import FakeTokenProvider


def test_get_token() -> None:
    provider = FakeTokenProvider()

    manager = TokenManager(provider)

    assert manager.get_token() == "fake-token"
