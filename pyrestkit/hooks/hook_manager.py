from __future__ import annotations

from typing import Any

import requests

from pyrestkit.hooks.hook import Hook


class HookManager:
    """
    Executes registered hooks.
    """

    def __init__(
        self,
        hooks: list[Hook] | None = None,
    ) -> None:
        self._hooks = hooks or []

    def before_request(
        self,
        method: str,
        url: str,
        kwargs: dict[str, Any],
    ) -> None:
        for hook in self._hooks:
            hook.before_request(
                method,
                url,
                kwargs,
            )

    def after_response(
        self,
        response: requests.Response,
    ) -> None:
        for hook in self._hooks:
            hook.after_response(response)
