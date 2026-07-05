from __future__ import annotations

from typing import Any

from pyrestkit.ai.config import AIConfig
from pyrestkit.ai.exceptions import AIConfigurationError, AIProviderError
from pyrestkit.ai.providers.base import BaseAIProvider


class MistralProvider(BaseAIProvider):
    """
    Mistral provider using the chat/completions endpoint.
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
            raise AIConfigurationError("Mistral API key is required.")

        payload: dict[str, Any] = {
            "model": config.model,
            "messages": [{"role": "user", "content": prompt}],
        }

        if system_prompt:
            payload["messages"].insert(0, {"role": "system", "content": system_prompt})

        response = self._session.post(
            _chat_url(config.base_url),
            json=payload,
            headers=_headers(config),
            timeout=config.timeout,
        )

        if response.status_code >= 400:
            raise AIProviderError(
                f"Mistral request failed with status {response.status_code}: "
                f"{response.text}"
            )

        try:
            data = response.json()
        except ValueError as exc:
            raise AIProviderError("Mistral response was not valid JSON.") from exc

        if not isinstance(data, dict):
            raise AIProviderError("Mistral response was not a JSON object.")

        choices = data.get("choices")
        if isinstance(choices, list) and choices:
            first = choices[0]
            if isinstance(first, dict):
                message = first.get("message")
                if isinstance(message, dict):
                    content = message.get("content")
                    if isinstance(content, str):
                        return content

        raise AIProviderError("Mistral response did not include text content.")


def _chat_url(base_url: str | None) -> str:
    base = (base_url or "https://api.mistral.ai/v1").rstrip("/")
    return f"{base}/chat/completions"


def _headers(config: AIConfig) -> dict[str, str]:
    headers: dict[str, str] = {
        "Content-Type": "application/json",
    }

    if config.api_key is not None:
        headers["Authorization"] = f"Bearer {config.api_key}"

    if config.organization is not None:
        headers["OpenAI-Organization"] = config.organization

    headers.update(config.headers)

    return headers
