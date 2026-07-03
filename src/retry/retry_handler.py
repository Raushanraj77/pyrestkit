from __future__ import annotations

from collections.abc import Callable
from typing import Any

import requests

from src.retry.backoff import ExponentialBackoff
from src.retry.retry_policy import RetryPolicy


class RetryHandler:
    """
    Executes HTTP requests with retry support.
    """

    def __init__(
        self,
        policy: RetryPolicy,
    ) -> None:
        self._policy = policy
        self._backoff = ExponentialBackoff(
            factor=policy.backoff_factor,
        )

    def execute(
        self,
        request: Callable[..., requests.Response],
        **kwargs: Any,
    ) -> requests.Response:
        last_exception: Exception | None = None

        for attempt in range(
            1,
            self._policy.retries + 1,
        ):
            try:
                response = request(**kwargs)

                if response.status_code not in self._policy.retry_on_status:
                    return response

            except self._policy.retry_on_exceptions as exc:
                last_exception = exc

            if attempt < self._policy.retries:
                self._backoff.sleep(attempt)

        if last_exception is not None:
            raise last_exception

        return response
