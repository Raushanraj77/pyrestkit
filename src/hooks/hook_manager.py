from __future__ import annotations

from typing import Any

import requests

from src.hooks.request_hook import RequestHook
from src.hooks.response_hook import ResponseHook


class HookManager:
    """
    Registers and executes request and response hooks.
    """

    def __init__(self) -> None:
        self._request_hooks: list[RequestHook] = []
        self._response_hooks: list[ResponseHook] = []

    def add_request_hook(
        self,
        hook: RequestHook,
    ) -> None:
        self._request_hooks.append(hook)

    def add_response_hook(
        self,
        hook: ResponseHook,
    ) -> None:
        self._response_hooks.append(hook)

    def execute_before_request(
        self,
        method: str,
        url: str,
        kwargs: dict[str, Any],
    ) -> None:
        for hook in self._request_hooks:
            hook.before_request(
                method,
                url,
                kwargs,
            )

    def execute_after_response(
        self,
        response: requests.Response,
    ) -> None:
        for hook in self._response_hooks:
            hook.after_response(response)
