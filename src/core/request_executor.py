from __future__ import annotations

from typing import Any

import requests

from src.core.logger import FrameworkLogger
from src.core.session_manager import SessionManager
from src.hooks.hook_manager import HookManager


class RequestExecutor:
    """
    Executes HTTP requests using the configured session.
    """

    def __init__(
        self,
        session_manager: SessionManager,
        hook_manager: HookManager | None = None,
    ) -> None:
        self._session = session_manager.session
        self._logger = FrameworkLogger.get_logger()
        self._hook_manager = hook_manager or HookManager()

    def execute(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> requests.Response:
        self._logger.info("%s %s", method.upper(), url)

        response = self._session.request(
            method=method,
            url=url,
            **kwargs,
        )

        self._logger.info(
            "Status Code: %s | Response Time: %.2f ms",
            response.status_code,
            response.elapsed.total_seconds() * 1000,
        )

        return response
