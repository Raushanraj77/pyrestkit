from __future__ import annotations

from typing import Any

import requests

from src.auth.authentication_manager import AuthenticationManager
from src.config.config import ConfigManager
from src.core.logger import FrameworkLogger
from src.core.session_manager import SessionManager


class APIClient:
    """
    Generic HTTP client for the automation framework.
    """

    def __init__(
        self,
        config: ConfigManager,
        session_manager: SessionManager,
        auth_manager: AuthenticationManager | None = None,
    ) -> None:
        self._config = config
        self._session = session_manager.session
        self._auth_manager = auth_manager
        self._logger = FrameworkLogger.get_logger()

    def _send_request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> requests.Response:

        url = "/".join(
            [
                self._config.base_url.rstrip("/"),
                endpoint.lstrip("/"),
            ]
        )

        headers = self._config.headers.copy()

        if self._auth_manager is not None:
            headers.update(self._auth_manager.get_headers())

        custom_headers = kwargs.pop(
            "headers",
            {},
        )

        headers.update(custom_headers)

        timeout = kwargs.pop(
            "timeout",
            self._config.timeout,
        )

        request_kwargs = {
            "headers": headers,
            "timeout": timeout,
            **kwargs,
        }

        self._logger.info(
            "Request: %s %s",
            method.upper(),
            url,
        )

        response = self._session.request(
            method=method,
            url=url,
            **request_kwargs,
        )

        self._logger.info(
            "Response: %s | %.2f ms",
            response.status_code,
            response.elapsed.total_seconds() * 1000,
        )

        return response

    def get(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self._send_request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self._send_request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self._send_request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self._send_request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self._send_request("DELETE", endpoint, **kwargs)
