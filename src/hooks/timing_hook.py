from __future__ import annotations

import time
from typing import Any

import requests

from src.hooks.hook import Hook


class TimingHook(Hook):
    """
    Measures request execution time.
    """

    def __init__(self) -> None:
        self._start = 0.0

    def before_request(
        self,
        method: str,
        url: str,
        kwargs: dict[str, Any],
    ) -> None:
        self._start = time.perf_counter()

    def after_response(
        self,
        response: requests.Response,
    ) -> None:
        elapsed = (time.perf_counter() - self._start) * 1000
        print(f"Request completed in {elapsed:.2f} ms")
