from __future__ import annotations

from typing import Any

from pyrestkit.ai.config import AIConfig
from pyrestkit.ai.exceptions import AIConfigurationError, AIProviderError
from pyrestkit.ai.providers.base import BaseAIProvider


class BedrockProvider(BaseAIProvider):
    """
    AWS Bedrock provider using a simple text-generation style payload.
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
            raise AIConfigurationError("Bedrock API key is required.")

        payload: dict[str, Any] = {
            "model": config.model,
            "inputText": prompt,
        }

        if system_prompt:
            payload["systemPrompt"] = system_prompt

        response = self._session.post(
            _invoke_url(config.base_url),
            json=payload,
            headers=_headers(config),
            timeout=config.timeout,
        )

        if response.status_code >= 400:
            raise AIProviderError(
                f"Bedrock request failed with status {response.status_code}: "
                f"{response.text}"
            )

        try:
            data = response.json()
        except ValueError as exc:
            raise AIProviderError("Bedrock response was not valid JSON.") from exc

        if not isinstance(data, dict):
            raise AIProviderError("Bedrock response was not a JSON object.")

        output = data.get("outputText")
        if isinstance(output, str) and output.strip():
            return output

        raise AIProviderError("Bedrock response did not include text content.")


def _invoke_url(base_url: str | None) -> str:
    base = (base_url or "https://bedrock-runtime.us-east-1.amazonaws.com").rstrip("/")
    return f"{base}/model:invoke"


def _headers(config: AIConfig) -> dict[str, str]:
    return BaseAIProvider.json_headers(config)
