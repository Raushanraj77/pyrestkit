from __future__ import annotations

from typing import Any

import requests

from src.auth.auth_strategy import AuthenticationStrategy
from src.config.config import ConfigManager
from src.core.request_builder import RequestBuilder
from src.core.request_executor import RequestExecutor
from src.core.session_manager import SessionManager
from src.hooks.hook_manager import HookManager


class APIClient:
    """
    Generic HTTP client for the automation framework.
    """

    def __init__(
        self,
        config: ConfigManager,
        session_manager: SessionManager,
        auth_strategy: AuthenticationStrategy | None = None,
        hook_manager: HookManager | None = None,
    ) -> None:
        self._builder = RequestBuilder(
            config=config,
            auth_strategy=auth_strategy,
        )

        self._executor = RequestExecutor(
            config=config,
            session_manager=session_manager,
            hook_manager=hook_manager,
        )

    def _send_request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> requests.Response:
        url, kwargs = self._builder.build(
            endpoint,
            **kwargs,
        )

        return self._executor.execute(
            method=method,
            url=url,
            **kwargs,
        )

    def get(
        self,
        endpoint: str,
        **kwargs: Any,
    ) -> requests.Response:
        return self._send_request(
            "GET",
            endpoint,
            **kwargs,
        )

    def post(
        self,
        endpoint: str,
        **kwargs: Any,
    ) -> requests.Response:
        return self._send_request(
            "POST",
            endpoint,
            **kwargs,
        )

    def put(
        self,
        endpoint: str,
        **kwargs: Any,
    ) -> requests.Response:
        return self._send_request(
            "PUT",
            endpoint,
            **kwargs,
        )

    def patch(
        self,
        endpoint: str,
        **kwargs: Any,
    ) -> requests.Response:
        return self._send_request(
            "PATCH",
            endpoint,
            **kwargs,
        )

    def delete(
        self,
        endpoint: str,
        **kwargs: Any,
    ) -> requests.Response:
        return self._send_request(
            "DELETE",
            endpoint,
            **kwargs,
        )
