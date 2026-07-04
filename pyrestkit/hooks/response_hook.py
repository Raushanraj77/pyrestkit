from __future__ import annotations

from abc import ABC, abstractmethod

import requests


class ResponseHook(ABC):
    """
    Executed after an HTTP response is received.
    """

    @abstractmethod
    def after_response(
        self,
        response: requests.Response,
    ) -> None: ...
