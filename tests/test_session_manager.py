import requests

from src.core.session_manager import SessionManager


def test_session_creation():
    manager = SessionManager()

    assert isinstance(manager.session, requests.Session)

    manager.close()