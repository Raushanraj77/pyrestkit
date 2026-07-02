from __future__ import annotations

from src.auth.token_provider import TokenProvider


class TokenManager:
    """
    Responsible for retrieving access tokens.

    Caching and refresh logic will be added in later modules.
    """

    def __init__(
        self,
        provider: TokenProvider,
    ) -> None:
        self._provider = provider

    def get_token(self) -> str:
        """
        Return an access token.
        """
        return self._provider.get_token()
