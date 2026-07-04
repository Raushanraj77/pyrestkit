from collections.abc import Generator

import pytest

from pyrestkit.auth.token_cache import TokenCache
from pyrestkit.auth.token_manager import TokenManager
from pyrestkit.clients.user_client import UserClient
from pyrestkit.config.config import ConfigManager
from pyrestkit.core.api_client import APIClient
from pyrestkit.core.session_manager import SessionManager
from tests.fake_token_provider import FakeTokenProvider


@pytest.fixture
def token_cache() -> TokenCache:
    return TokenCache()


@pytest.fixture
def token_manager(
    token_cache: TokenCache,
) -> TokenManager:
    provider = FakeTokenProvider()

    return TokenManager(
        provider=provider,
        cache=token_cache,
    )


# @pytest.fixture
# def token_manager() -> TokenManager:
#     return TokenManager(FakeTokenProvider(), cache=cache)  # type: ignore


@pytest.fixture(scope="session")
def config() -> ConfigManager:
    return ConfigManager("dev")


@pytest.fixture(scope="session")
def session_manager() -> Generator[SessionManager]:
    manager = SessionManager()

    try:
        yield manager
    finally:
        manager.close()


@pytest.fixture(scope="session")
def api_client(
    config: ConfigManager,
    session_manager: SessionManager,
) -> APIClient:
    return APIClient(
        config=config,
        session_manager=session_manager,
    )


@pytest.fixture
def user_client(api_client: APIClient) -> UserClient:
    return UserClient(api_client)
