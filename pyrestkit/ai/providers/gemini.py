from __future__ import annotations

from typing import Any

from pyrestkit.ai.config import AIConfig
from pyrestkit.ai.exceptions import AIConfigurationError, AIProviderError
from pyrestkit.ai.providers.base import BaseAIProvider


class GeminiProvider(BaseAIProvider):
    """
    Google Gemini provider using the generateContent endpoint.
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
            raise AIConfigurationError("Gemini API key is required.")

        content: dict[str, Any] = {
            "parts": [
                {
                    "text": prompt,
                }
            ]
        }

        payload: dict[str, Any] = {
            "contents": [content],
        }

        if system_prompt:
            payload["system_instruction"] = {
                "parts": [
                    {
                        "text": system_prompt,
                    }
                ]
            }

        response = self._session.post(
            _generate_url(config.base_url),
            json=payload,
            headers=_headers(config),
            timeout=config.timeout,
        )

        if response.status_code >= 400:
            raise AIProviderError(
                f"Gemini request failed with status "
                f"{response.status_code}: {response.text}"
            )

        try:
            data = response.json()
        except ValueError as exc:
            raise AIProviderError("Gemini response was not valid JSON.") from exc

        if not isinstance(data, dict):
            raise AIProviderError("Gemini response was not a JSON object.")

        candidates = data.get("candidates")

        if isinstance(candidates, list):
            for candidate in candidates:
                if not isinstance(candidate, dict):
                    continue

                candidate_content = candidate.get("content")
                if not isinstance(candidate_content, dict):
                    continue

                parts = candidate_content.get("parts")
                if not isinstance(parts, list):
                    continue

                texts: list[str] = []

                for part in parts:
                    if not isinstance(part, dict):
                        continue

                    text = part.get("text")
                    if isinstance(text, str):
                        texts.append(text)

                if texts:
                    return "\n".join(texts)

        raise AIProviderError("Gemini response did not include text content.")


def _generate_url(base_url: str | None) -> str:
    base = (base_url or "https://generativelanguage.googleapis.com/v1beta").rstrip("/")

    return f"{base}/models/gemini-2.0-flash:generateContent"


def _headers(config: AIConfig) -> dict[str, str]:
    headers = BaseAIProvider.json_headers(config)

    if config.api_key is not None:
        headers["x-goog-api-key"] = config.api_key

    return headers
