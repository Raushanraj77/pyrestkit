from __future__ import annotations

import time


class ExponentialBackoff:
    """
    Implements exponential backoff.

    Example:

    attempt=1 -> 1 sec

    attempt=2 -> 2 sec

    attempt=3 -> 4 sec

    attempt=4 -> 8 sec
    """

    def __init__(
        self,
        factor: float = 1.0,
    ) -> None:
        self._factor = factor

    def sleep(
        self,
        attempt: int,
    ) -> None:
        delay = self._factor * (2 ** (attempt - 1))
        time.sleep(delay)
