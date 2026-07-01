import requests

from src.core.session_manager import SessionManager


def test_session_creation():
    session_manager = SessionManager()

    assert isinstance(session_manager.session, requests.Session)

    session_manager.close()


def test_close_session():
    session_manager = SessionManager()

    session_manager.close()

    #assert session_manager.session is None