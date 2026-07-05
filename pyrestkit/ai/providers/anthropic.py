from __future__ import annotations

from typing import Any

from pyrestkit.ai.config import AIConfig
from pyrestkit.ai.exceptions import AIConfigurationError, AIProviderError
from pyrestkit.ai.providers.base import BaseAIProvider


class AnthropicProvider(BaseAIProvider):
    """
    Anthropic provider using the Messages API.
    """

    def __init__(self, session: Any | None = None) -> None:
        super().__init__(session=session)

    def complete(
        self,
        prompt: str,
        *,
        config: AIConfig,
        system_prompt: str | None = None,
    ) -> str:
        if not config.api_key:
            raise AIConfigurationError("Anthropic API key is required.")

        payload: dict[str, Any] = {
            "model": config.model,
            "max_tokens": config.max_tokens or 1024,
            "messages": [{"role": "user", "content": prompt}],
        }

        if system_prompt:
            payload["system"] = system_prompt

        response = self._session.post(
            _messages_url(config.base_url),
            json=payload,
            headers=_headers(config),
            timeout=config.timeout,
        )

        if response.status_code >= 400:
            raise AIProviderError(
                f"Anthropic request failed with status {response.status_code}: "
                f"{response.text}"
            )

        try:
            data = response.json()
        except ValueError as exc:
            raise AIProviderError("Anthropic response was not valid JSON.") from exc

        if not isinstance(data, dict):
            raise AIProviderError("Anthropic response was not a JSON object.")

        content = data.get("content")
        if isinstance(content, list):
            parts: list[str] = []
            for item in content:
                if isinstance(item, dict):
                    text = item.get("text")
                    if isinstance(text, str):
                        parts.append(text)
            if parts:
                return "\n".join(parts)

        raise AIProviderError("Anthropic response did not include text content.")


def _messages_url(base_url: str | None) -> str:
    base = (base_url or "https://api.anthropic.com/v1").rstrip("/")
    return f"{base}/messages"


def _headers(config: AIConfig) -> dict[str, str]:
    headers = BaseAIProvider.json_headers(config)

    headers["anthropic-version"] = "2023-06-01"

    if config.api_key is not None:
        headers["x-api-key"] = config.api_key

    return headers
