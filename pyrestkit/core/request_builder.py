from __future__ import annotations

from typing import Any

from pyrestkit.auth.auth_strategy import AuthenticationStrategy
from pyrestkit.config.config import ConfigManager


class RequestBuilder:
    """
    Builds request arguments for the API client.
    """

    def __init__(
        self,
        config: ConfigManager,
        auth_strategy: AuthenticationStrategy | None = None,
    ) -> None:
        self._config = config
        self._auth_strategy = auth_strategy

    def build(
        self,
        endpoint: str,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any]]:
        url = f"{self._config.base_url}{endpoint}"

        headers = self._config.headers.copy()

        if self._auth_strategy is not None:
            headers.update(self._auth_strategy.get_headers())

        request_headers = kwargs.pop("headers", {})
        headers.update(request_headers)

        timeout = kwargs.pop(
            "timeout",
            self._config.timeout,
        )

        kwargs["headers"] = headers
        kwargs["timeout"] = timeout

        return url, kwargs
