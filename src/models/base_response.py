from __future__ import annotations

from typing import Any, Protocol, Self


class BaseResponse(Protocol):
    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> Self: ...
