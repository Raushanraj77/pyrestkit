from abc import ABC, abstractmethod

from src.auth.token_response import TokenResponse


class TokenProvider(ABC):
    @abstractmethod
    def get_token(self) -> TokenResponse:
        """
        Fetch a new token.
        """
        raise NotImplementedError
