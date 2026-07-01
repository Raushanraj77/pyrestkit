from __future__ import annotations

import requests


class SessionManager:
    """
    Creates and manages HTTP sessions for the framework.
    """

    def __init__(self) -> None:
        self._session = requests.Session()

    @property
    def session(self) -> requests.Session:
        return self._session

    def close(self) -> None:
        self._session.close()