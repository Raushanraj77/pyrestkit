from __future__ import annotations

from pyrestkit.auth.token_cache import TokenCache
from pyrestkit.auth.token_provider import TokenProvider


class TokenManager:
    """
    Responsible for retrieving access tokens.

    Caching and refresh logic will be added in later modules.
    """

    def __init__(
        self,
        provider: TokenProvider,
        cache: TokenCache,
    ) -> None:
        self._provider = provider
        self._cache = cache

    def get_token(self) -> str:
        cached = self._cache.get()

        if cached is not None:
            return cached.access_token

        response = self._provider.get_token()

        self._cache.set(response)

        return response.access_token
