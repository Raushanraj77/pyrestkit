from __future__ import annotations

from typing import Any

import requests

from pyrestkit.auth.auth_strategy import AuthenticationStrategy
from pyrestkit.config.config import ConfigManager
from pyrestkit.core.logger import FrameworkLogger
from pyrestkit.core.session_manager import SessionManager
from pyrestkit.retry.retry_handler import RetryHandler
from pyrestkit.retry.retry_policy import RetryPolicy


class APIClient:
    """
    Generic HTTP client for the automation framework.
    """

    def __init__(
        self,
        config: ConfigManager,
        session_manager: SessionManager,
        auth_strategy: AuthenticationStrategy | None = None,
        retry_policy: RetryPolicy | None = None,
    ) -> None:
        self._config = config
        self._session = session_manager.session
        self._auth_strategy = auth_strategy
        self._logger = FrameworkLogger.get_logger()

        self._retry_handler = RetryHandler(
            retry_policy or RetryPolicy(),
        )

    def _build_headers(
        self,
        custom_headers: dict[str, str] | None,
    ) -> dict[str, str]:
        headers = self._config.headers.copy()

        if self._auth_strategy is not None:
            headers.update(
                self._auth_strategy.get_headers(),
            )

        if custom_headers:
            headers.update(custom_headers)

        return headers

    def _send_request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> requests.Response:
        url = f"{self._config.base_url}{endpoint}"

        headers = self._build_headers(
            kwargs.pop("headers", None),
        )

        timeout = kwargs.pop(
            "timeout",
            self._config.timeout,
        )

        kwargs["headers"] = headers
        kwargs["timeout"] = timeout

        self._logger.info("%s %s", method.upper(), url)

        response = self._retry_handler.execute(
            self._session.request,
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
