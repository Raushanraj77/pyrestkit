from collections.abc import Generator

import pytest

from src.clients.user_client import UserClient
from src.config.config import ConfigManager
from src.core.api_client import APIClient
from src.core.session_manager import SessionManager


@pytest.fixture(scope="session")
def config() -> ConfigManager:
    return ConfigManager("dev")


@pytest.fixture(scope="session")
def session_manager() -> Generator[SessionManager, None, None]:
    manager = SessionManager()

    yield manager

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