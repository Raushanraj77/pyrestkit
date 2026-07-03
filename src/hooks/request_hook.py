from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class RequestHook(ABC):
    """
    Executed before an HTTP request is sent.
    """

    @abstractmethod
    def before_request(
        self,
        method: str,
        url: str,
        kwargs: dict[str, Any],
    ) -> None: ...
