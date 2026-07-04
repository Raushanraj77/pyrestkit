from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TokenResponse:
    """
    Represents an authentication token returned by the auth server.
    """

    access_token: str
    expires_in: int
