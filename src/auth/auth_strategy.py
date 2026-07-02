from __future__ import annotations

from abc import ABC, abstractmethod


class AuthenticationStrategy(ABC):
    """Base interface for all authentication strategies.
    This is the interface every authentication implementation must follow.
    """

    @abstractmethod
    def get_headers(self) -> dict[str, str]:
        """Return authentication headers."""
        raise NotImplementedError
