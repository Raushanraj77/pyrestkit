from pyrestkit.pipeline.middleware import Middleware
from pyrestkit.pipeline.request_context import RequestContext


class RequestPipeline:
    """
    Executes middleware sequentially.
    """

    def __init__(self) -> None:
        self._middlewares: list[Middleware] = []

    def add(
        self,
        middleware: Middleware,
    ) -> None:
        self._middlewares.append(middleware)

    def execute(
        self,
        context: RequestContext,
    ) -> RequestContext:

        for middleware in self._middlewares:
            context = middleware.process(context)

        return context
