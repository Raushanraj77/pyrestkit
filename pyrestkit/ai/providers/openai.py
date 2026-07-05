from __future__ import annotations

from typing import Any

from pyrestkit.ai.config import AIConfig
from pyrestkit.ai.exceptions import AIConfigurationError, AIProviderError
from pyrestkit.ai.providers.base import BaseAIProvider


class OpenAIResponsesProvider(BaseAIProvider):
    """
    OpenAI provider backed by the Responses API.
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
        if not config.api_key:
            raise AIConfigurationError("OpenAI API key is required.")

        payload: dict[str, Any] = {
            "model": config.model,
            "input": prompt,
            "temperature": config.temperature,
        }

        if system_prompt:
            payload["instructions"] = system_prompt

        if config.max_tokens is not None:
            payload["max_output_tokens"] = config.max_tokens

        response = self._session.post(
            _responses_url(config.base_url),
            json=payload,
            headers=_headers(config),
            timeout=config.timeout,
        )

        if response.status_code >= 400:
            raise AIProviderError(
                f"OpenAI request failed with status {response.status_code}: "
                f"{response.text}"
            )

        try:
            data = response.json()
        except ValueError as exc:
            raise AIProviderError("OpenAI response was not valid JSON.") from exc

        return _extract_text(data)


def _responses_url(
    base_url: str | None,
) -> str:
    base = (base_url or "https://api.openai.com/v1").rstrip("/")

    if base.endswith("/responses"):
        return base

    return f"{base}/responses"


def _headers(config: AIConfig) -> dict[str, str]:
    headers = BaseAIProvider.json_headers(config)

    if config.api_key is not None:
        headers["Authorization"] = f"Bearer {config.api_key}"

    if config.organization is not None:
        headers["OpenAI-Organization"] = config.organization

    return headers


def _extract_text(
    data: MappingLike,
) -> str:
    output_text = data.get("output_text")

    if isinstance(output_text, str) and output_text.strip():
        return output_text

    output = data.get("output", [])

    if isinstance(output, list):
        chunks: list[str] = []

        for item in output:
            if not isinstance(item, dict):
                continue

            content = item.get("content", [])

            if not isinstance(content, list):
                continue

            for part in content:
                if not isinstance(part, dict):
                    continue

                text = part.get("text")

                if isinstance(text, str):
                    chunks.append(text)

        if chunks:
            return "\n".join(chunks)

    raise AIProviderError("OpenAI response did not include output text.")


MappingLike = dict[str, Any]
