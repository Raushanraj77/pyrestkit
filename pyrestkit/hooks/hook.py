from __future__ import annotations

from typing import Any

import requests


class Hook:
    """
    Base class for framework hooks.

    Override only the callbacks you need.
    """

    def before_request(
        self,
        method: str,
        url: str,
        kwargs: dict[str, Any],
    ) -> None:
        return

    def after_response(
        self,
        response: requests.Response,
    ) -> None:
        return
