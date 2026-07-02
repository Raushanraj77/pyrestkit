from __future__ import annotations

from abc import ABC, abstractmethod


class TokenProvider(ABC):
    """
    Provides authentication tokens.
    """

    @abstractmethod
    def get_token(self) -> str:
        """
        Fetch a new access token.
        """
        raise NotImplementedError
