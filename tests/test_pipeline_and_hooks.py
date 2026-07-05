from __future__ import annotations

import requests

from pyrestkit.hooks.hook import Hook
from pyrestkit.hooks.hook_manager import HookManager
from pyrestkit.pipeline.middleware_chain import MiddlewareChain
from pyrestkit.pipeline.request_context import RequestContext


class RecordingHook(Hook):
    def __init__(self) -> None:
        self.calls: list[str] = []

    def before_request(self, method: str, url: str, kwargs: dict) -> None:
        self.calls.append(f"before:{method}:{url}")

    def after_response(self, response: requests.Response) -> None:
        self.calls.append(f"after:{response.status_code}")


def test_middleware_chain_builds_pipeline() -> None:
    pipeline = MiddlewareChain.build()

    assert pipeline is not None


def test_hook_manager_executes_callbacks() -> None:
    hook = RecordingHook()
    manager = HookManager([hook])
    response = requests.Response()
    response.status_code = 200

    manager.before_request("GET", "https://example.com", {})
    manager.after_response(response)

    assert hook.calls == ["before:GET:https://example.com", "after:200"]


def test_request_context_defaults() -> None:
    context = RequestContext(method="GET", url="https://example.com")

    assert context.timeout == 30
    assert context.json is None
    assert context.data is None
