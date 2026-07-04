from __future__ import annotations

from typing import Any

from src.config.config import ConfigManager
from src.core.logger import FrameworkLogger
from src.core.session_manager import SessionManager
from src.exceptions.exception_mapper import ExceptionMapper
from src.hooks.hook_manager import HookManager
from src.response.framework_response import FrameworkResponse


class RequestExecutor:
    """
    Executes HTTP requests using the configured session.
    """

    def __init__(
        self,
        config: ConfigManager,
        session_manager: SessionManager,
        hook_manager: HookManager | None = None,
    ) -> None:
        self._config = config
        self._session = session_manager.session
        self._logger = FrameworkLogger.get_logger()
        self._hook_manager = hook_manager or HookManager()

    def execute(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> FrameworkResponse:
        self._logger.info(
            "%s %s",
            method.upper(),
            url,
        )

        self._hook_manager.before_request(
            method=method,
            url=url,
            kwargs=kwargs,
        )

        response = self._session.request(
            method=method,
            url=url,
            **kwargs,
        )

        self._hook_manager.after_response(response)

        if self._config.auto_raise_exceptions:
            ExceptionMapper.raise_for_response(response)

        self._logger.info(
            "Status Code: %s | Response Time: %.2f ms",
            response.status_code,
            response.elapsed.total_seconds() * 1000,
        )

        return FrameworkResponse(response)
