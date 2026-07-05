from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import requests

from pyrestkit.ai.config import AIConfig


class BaseAIProvider(ABC):
    """
    Base class for all AI providers.
    """

    def __init__(self, session: Any | None = None) -> None:
        self._session = session or requests.Session()

    @staticmethod
    def json_headers(config: AIConfig) -> dict[str, str]:
        """
        Build common JSON headers.
        """
        headers: dict[str, str] = {
            "Content-Type": "application/json",
        }

        headers.update(config.headers)

        return headers

    @abstractmethod
    def complete(
        self,
        prompt: str,
        *,
        config: AIConfig,
        system_prompt: str | None = None,
    ) -> str: ...
