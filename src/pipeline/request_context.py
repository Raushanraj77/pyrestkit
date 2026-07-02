from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RequestContext:
    """
    Represents a single HTTP request flowing through the middleware pipeline.
    """

    method: str
    url: str

    headers: dict[str, str] = field(default_factory=dict)

    params: dict[str, Any] = field(default_factory=dict)

    json: dict[str, Any] | None = None

    data: Any = None

    timeout: int = 30

    kwargs: dict[str, Any] = field(default_factory=dict)
