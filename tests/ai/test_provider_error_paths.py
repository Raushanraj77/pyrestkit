from __future__ import annotations

import pytest

from pyrestkit.ai.config import AIConfig
from pyrestkit.ai.exceptions import AIConfigurationError, AIProviderError
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
        payload: object,
        status_code: int = 200,
        text: str = "",
    ) -> None:
        self._payload = payload
        self.status_code = status_code
        self.text = text

    def json(self) -> object:
        return self._payload


class FakeSession:
    def __init__(self, response: FakeResponse) -> None:
        self.response = response

    def post(
        self, url: str, *, json: dict, headers: dict, timeout: int
    ) -> FakeResponse:
        return self.response


@pytest.mark.parametrize(
    ("provider_cls", "base_url_value"),
    [
        (AnthropicProvider, "https://api.anthropic.com/v1"),
        (AzureOpenAIProvider, "https://example.openai.azure.com"),
        (BedrockProvider, "https://bedrock-runtime.us-east-1.amazonaws.com"),
        (CohereProvider, "https://api.cohere.com/v1"),
        (GeminiProvider, "https://generativelanguage.googleapis.com/v1beta"),
        (GroqProvider, "https://api.groq.com/openai/v1"),
        (MistralProvider, "https://api.mistral.ai/v1"),
        (OllamaProvider, "http://localhost:11434"),
    ],
)
def test_ai_provider_requires_api_key(
    provider_cls: type[BaseAIProvider],
    base_url_value: str,
) -> None:
    provider = provider_cls(session=FakeSession(FakeResponse({})))
    config = AIConfig(provider="test", model="model", base_url=base_url_value)

    expected_exception: type[AIConfigurationError] | type[AIProviderError]

    if provider_cls is OllamaProvider:
        expected_exception = AIProviderError
    else:
        expected_exception = AIConfigurationError

    with pytest.raises(expected_exception):
        provider.complete("Analyze", config=config)


@pytest.mark.parametrize(
    ("provider_cls", "base_url_value"),
    [
        (AnthropicProvider, "https://api.anthropic.com/v1"),
        (AzureOpenAIProvider, "https://example.openai.azure.com"),
        (BedrockProvider, "https://bedrock-runtime.us-east-1.amazonaws.com"),
        (CohereProvider, "https://api.cohere.com/v1"),
        (GeminiProvider, "https://generativelanguage.googleapis.com/v1beta"),
        (GroqProvider, "https://api.groq.com/openai/v1"),
        (MistralProvider, "https://api.mistral.ai/v1"),
        (OllamaProvider, "http://localhost:11434"),
    ],
)
def test_ai_provider_raises_on_invalid_payload(
    provider_cls: type[BaseAIProvider],
    base_url_value: str,
) -> None:
    provider = provider_cls(session=FakeSession(FakeResponse([])))
    config = AIConfig(
        provider="test",
        model="model",
        api_key="key",
        base_url=base_url_value,
    )

    with pytest.raises(AIProviderError):
        provider.complete("Analyze", config=config)


@pytest.mark.parametrize(
    ("provider_cls", "base_url_value"),
    [
        (AnthropicProvider, "https://api.anthropic.com/v1"),
        (AzureOpenAIProvider, "https://example.openai.azure.com"),
        (BedrockProvider, "https://bedrock-runtime.us-east-1.amazonaws.com"),
        (CohereProvider, "https://api.cohere.com/v1"),
        (GeminiProvider, "https://generativelanguage.googleapis.com/v1beta"),
        (GroqProvider, "https://api.groq.com/openai/v1"),
        (MistralProvider, "https://api.mistral.ai/v1"),
        (OllamaProvider, "http://localhost:11434"),
    ],
)
def test_ai_provider_raises_on_http_error(
    provider_cls: type[BaseAIProvider],
    base_url_value: str,
) -> None:
    provider = provider_cls(
        session=FakeSession(FakeResponse({}, status_code=500, text="boom"))
    )
    config = AIConfig(
        provider="test",
        model="model",
        api_key="key",
        base_url=base_url_value,
    )

    with pytest.raises(AIProviderError, match="failed with status"):
        provider.complete("Analyze", config=config)
