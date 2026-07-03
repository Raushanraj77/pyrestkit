from __future__ import annotations

from dataclasses import dataclass, field

import requests


@dataclass(slots=True)
class RetryPolicy:
    """
    Retry configuration.
    """

    retries: int = 3

    backoff_factor: float = 1.0

    retry_on_status: set[int] = field(
        default_factory=lambda: {
            500,
            502,
            503,
            504,
        },
    )

    retry_on_exceptions: tuple[
        type[Exception],
        ...,
    ] = (
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
    )
