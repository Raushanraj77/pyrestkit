from __future__ import annotations

from typing import Any

from pyrestkit.ai.config import AIConfig
from pyrestkit.ai.exceptions import AIConfigurationError, AIProviderError
from pyrestkit.ai.providers.base import BaseAIProvider


class CohereProvider(BaseAIProvider):
    """
    Cohere provider using the chat endpoint.
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
            raise AIConfigurationError("Cohere API key is required.")

        payload: dict[str, Any] = {
            "model": config.model,
            "message": prompt,
        }

        if system_prompt:
            payload["chat_history"] = [{"role": "SYSTEM", "message": system_prompt}]

        response = self._session.post(
            _chat_url(config.base_url),
            json=payload,
            headers=_headers(config),
            timeout=config.timeout,
        )

        if response.status_code >= 400:
            raise AIProviderError(
                f"Cohere request failed with status {response.status_code}: "
                f"{response.text}"
            )

        try:
            data = response.json()
        except ValueError as exc:
            raise AIProviderError("Cohere response was not valid JSON.") from exc

        if not isinstance(data, dict):
            raise AIProviderError("Cohere response was not a JSON object.")

        texts = data.get("text")
        if isinstance(texts, str) and texts.strip():
            return texts

        raise AIProviderError("Cohere response did not include text content.")


def _chat_url(base_url: str | None) -> str:
    base = (base_url or "https://api.cohere.com/v1").rstrip("/")
    return f"{base}/chat"


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
