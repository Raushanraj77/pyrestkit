from pyrestkit.pipeline.pipeline import RequestPipeline
from pyrestkit.pipeline.request_context import RequestContext


def test_empty_pipeline() -> None:
    pipeline = RequestPipeline()

    context = RequestContext(
        method="GET",
        url="https://reqres.in/api/users",
    )

    result = pipeline.execute(context)

    assert result.url == context.url
