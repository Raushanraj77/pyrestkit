from __future__ import annotations

from typing import Any

from pyrestkit.ai.config import AIConfig
from pyrestkit.ai.exceptions import AIProviderError
from pyrestkit.ai.providers.base import BaseAIProvider


class OllamaProvider(BaseAIProvider):
    """
    Local Ollama provider using the generate endpoint.
    """

    def __init__(
        self,
        session: Any | None = None,
    ) -> None:
        super().__init__(session=session)

    def complete(
        self,
        prompt: str,
        *,
        config: AIConfig,
        system_prompt: str | None = None,
    ) -> str:
        options: dict[str, Any] = {
            "temperature": config.temperature,
        }

        if config.max_tokens is not None:
            options["num_predict"] = config.max_tokens

        payload: dict[str, Any] = {
            "model": config.model,
            "prompt": prompt,
            "stream": False,
            "options": options,
        }

        if system_prompt:
            payload["system"] = system_prompt

        response = self._session.post(
            _generate_url(config.base_url),
            json=payload,
            headers=dict(config.headers),
            timeout=config.timeout,
        )

        if response.status_code >= 400:
            raise AIProviderError(
                f"Ollama request failed with status {response.status_code}: "
                f"{response.text}"
            )

        try:
            data = response.json()
        except ValueError as exc:
            raise AIProviderError("Ollama response was not valid JSON.") from exc

        if not isinstance(data, dict):
            raise AIProviderError("Ollama response was not a JSON object.")

        text = data.get("response")

        if not isinstance(text, str):
            raise AIProviderError("Ollama response did not include response text.")

        return text


def _generate_url(
    base_url: str | None,
) -> str:
    base = (base_url or "http://localhost:11434").rstrip("/")

    if base.endswith("/api/generate"):
        return base

    return f"{base}/api/generate"
