from __future__ import annotations

from abc import ABC, abstractmethod

from src.pipeline.request_context import RequestContext


class Middleware(ABC):
    """
    Base class for all middleware.
    """

    @abstractmethod
    def process(
        self,
        context: RequestContext,
    ) -> RequestContext:
        raise NotImplementedError
