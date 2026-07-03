from __future__ import annotations

from abc import ABC, abstractmethod

from src.pipeline.request_context import RequestContext


class Hook(ABC):
    """
    Base class for all framework hooks.
    """

    @abstractmethod
    def execute(self, context: RequestContext) -> None:
        """
        Execute the hook.
        """
        raise NotImplementedError
