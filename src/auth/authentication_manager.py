from __future__ import annotations

from src.auth.auth_strategy import AuthenticationStrategy


class AuthenticationManager:
    """
    Responsible for providing authentication headers.

    APIClient communicates only with this class and remains
    unaware of the underlying authentication mechanism.
    """

    def __init__(
        self,
        strategy: AuthenticationStrategy | None = None,
    ) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> AuthenticationStrategy | None:
        return self._strategy

    @strategy.setter
    def strategy(
        self,
        strategy: AuthenticationStrategy | None,
    ) -> None:
        self._strategy = strategy

    def get_headers(self) -> dict[str, str]:
        if self._strategy is None:
            return {}

        return self._strategy.get_headers()
