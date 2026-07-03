from __future__ import annotations

from datetime import UTC, datetime, timedelta
from threading import Lock

from src.auth.token_response import TokenResponse


class TokenCache:
    """
    Thread-safe cache for authentication tokens.
    """

    def __init__(self) -> None:
        self._response: TokenResponse | None = None
        self._expires_at: datetime | None = None
        self._lock = Lock()

    def get(self) -> TokenResponse | None:
        if self._response is None:
            return None

        if self._expires_at is None:
            return None

        if datetime.now(UTC) >= self._expires_at:
            return None

        return self._response

    def set(
        self,
        response: TokenResponse,
    ) -> None:
        with self._lock:
            self._response = response
            self._expires_at = datetime.now(UTC) + timedelta(
                seconds=response.expires_in,
            )

    def clear(self) -> None:
        with self._lock:
            self._response = None
            self._expires_at = None
