from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class FailureContext:
    """
    Normalized failure details that can be sent to an AI analyzer.
    """

    test_name: str
    file_path: str | None = None
    line_number: int | None = None
    error_type: str | None = None
    error_message: str | None = None
    traceback: str | None = None
    assertion: str | None = None
    expected: str | None = None
    actual: str | None = None
    request_method: str | None = None
    request_url: str | None = None
    response_status: int | None = None
    response_body: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class FailureAnalysis:
    """
    Structured AI output for a failing automation test.
    """

    summary: str
    likely_cause: str
    recommended_fix: str
    suggested_patch: str | None = None
    confidence: float = 0.0
    raw_response: str | None = None
