from __future__ import annotations

from typing import Any

import pytest

from pyrestkit.ai.config import AIConfig
from pyrestkit.ai.providers.anthropic import AnthropicProvider
from pyrestkit.ai.providers.azure_openai import AzureOpenAIProvider
from pyrestkit.ai.providers.base import BaseAIProvider
from pyrestkit.ai.providers.bedrock import BedrockProvider
from pyrestkit.ai.providers.cohere import CohereProvider
from pyrestkit.ai.providers.gemini import GeminiProvider
from pyrestkit.ai.providers.groq import GroqProvider
from pyrestkit.ai.providers.mistral import MistralProvider
from pyrestkit.ai.providers.ollama import OllamaProvider


class FakeResponse:
    def __init__(
        self,
        payload: dict[str, Any],
        status_code: int = 200,
        text: str = "",
    ) -> None:
        self._payload = payload
        self.status_code = status_code
        self.text = text

    def json(self) -> dict[str, Any]:
        return self._payload


class FakeSession:
    def __init__(self, response: FakeResponse) -> None:
        self.response = response
        self.url = ""
        self.payload: dict[str, Any] = {}
        self.headers: dict[str, str] = {}
        self.timeout = 0

    def post(
        self,
        url: str,
        *,
        json: dict[str, Any],
        headers: dict[str, str],
        timeout: int,
    ) -> FakeResponse:
        self.url = url
        self.payload = json
        self.headers = headers
        self.timeout = timeout
        return self.response


@pytest.mark.parametrize(
    ("provider_cls", "payload", "expected_text", "base_url_value", "expected_url"),
    [
        (
            AnthropicProvider,
            {"content": [{"text": "Anthropic response"}]},
            "Anthropic response",
            "https://api.anthropic.com/v1",
            "https://api.anthropic.com/v1/messages",
        ),
        (
            AzureOpenAIProvider,
            {"choices": [{"message": {"content": "Azure response"}}]},
            "Azure response",
            "https://example.openai.azure.com",
            "https://example.openai.azure.com/openai/deployments?api-version=2024-02-01",
        ),
        (
            BedrockProvider,
            {"outputText": "Bedrock response"},
            "Bedrock response",
            "https://bedrock-runtime.us-east-1.amazonaws.com",
            "https://bedrock-runtime.us-east-1.amazonaws.com/model:invoke",
        ),
        (
            CohereProvider,
            {"text": "Cohere response"},
            "Cohere response",
            "https://api.cohere.com/v1",
            "https://api.cohere.com/v1/chat",
        ),
        (
            GeminiProvider,
            {"candidates": [{"content": {"parts": [{"text": "Gemini response"}]}}]},
            "Gemini response",
            "https://generativelanguage.googleapis.com/v1beta",
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
        ),
        (
            GroqProvider,
            {"choices": [{"message": {"content": "Groq response"}}]},
            "Groq response",
            "https://api.groq.com/openai/v1",
            "https://api.groq.com/openai/v1/chat/completions",
        ),
        (
            MistralProvider,
            {"choices": [{"message": {"content": "Mistral response"}}]},
            "Mistral response",
            "https://api.mistral.ai/v1",
            "https://api.mistral.ai/v1/chat/completions",
        ),
        (
            OllamaProvider,
            {"response": "Ollama response"},
            "Ollama response",
            "http://localhost:11434",
            "http://localhost:11434/api/generate",
        ),
    ],
)
def test_provider_complete_returns_text(
    provider_cls: type[BaseAIProvider],
    payload: dict,
    expected_text: str,
    base_url_value: str,
    expected_url: str,
) -> None:
    session = FakeSession(FakeResponse(payload))
    provider = provider_cls(session=session)
    config = AIConfig(
        provider="test",
        model="test-model",
        api_key="key",
        base_url=base_url_value,
        timeout=30,
        max_tokens=128,
    )

    result = provider.complete(
        "Analyze this failure",
        config=config,
        system_prompt="You are helpful",
    )

    assert result == expected_text
    assert session.url == expected_url
    assert session.timeout == 30
