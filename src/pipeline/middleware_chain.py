from src.pipeline.pipeline import RequestPipeline


class MiddlewareChain:
    """
    Factory responsible for creating request pipelines.
    """

    @staticmethod
    def build() -> RequestPipeline:
        return RequestPipeline()
