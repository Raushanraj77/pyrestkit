from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class UserResponse:
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str
