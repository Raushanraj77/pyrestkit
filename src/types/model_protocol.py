from __future__ import annotations

from typing import Any, Protocol, TypeVar


class ModelProtocol(Protocol):
    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> ModelProtocol: ...


T = TypeVar(
    "T",
    bound=ModelProtocol,
)
