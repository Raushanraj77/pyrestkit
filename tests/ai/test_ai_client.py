from __future__ import annotations

import pytest

from pyrestkit.ai.client import AIClient, available_providers, register_provider
from pyrestkit.ai.config import AIConfig
from pyrestkit.ai.exceptions import AIConfigurationError
from pyrestkit.ai.provider import StaticAIProvider


def test_ai_client_delegates_to_provider() -> None:
    config = AIConfig(
        provider="openai",
        model="gpt-test",
    )
    provider = StaticAIProvider("analysis")
    client = AIClient(
        config=config,
        provider=provider,
    )

    result = client.complete(
        "Explain failure",
        system_prompt="Be concise",
    )

    assert result == "analysis"
    assert len(provider.calls) == 1
    assert provider.calls[0].prompt == "Explain failure"
    assert provider.calls[0].system_prompt == "Be concise"
    assert provider.calls[0].config == config


def test_ai_client_rejects_empty_prompt() -> None:
    config = AIConfig(
        provider="openai",
        model="gpt-test",
    )
    client = AIClient(
        config=config,
        provider=StaticAIProvider("analysis"),
    )

    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        client.complete(" ")


def test_ai_client_uses_registered_custom_provider() -> None:
    register_provider(
        "internal-llm",
        lambda: StaticAIProvider("custom analysis"),
    )

    config = AIConfig(
        provider="internal-llm",
        model="company-model",
    )
    client = AIClient(config)

    assert client.complete("Explain failure") == "custom analysis"
    assert "internal-llm" in available_providers()


def test_ai_client_requires_registered_provider() -> None:
    config = AIConfig(
        provider="not-installed",
        model="model",
    )

    with pytest.raises(AIConfigurationError, match="No AI provider registered"):
        AIClient(config)


def test_ai_client_registers_major_llm_providers() -> None:
    providers = set(available_providers())

    assert {
        "openai",
        "ollama",
        "anthropic",
        "gemini",
        "azure-openai",
        "cohere",
        "mistral",
        "groq",
        "bedrock",
    }.issubset(providers)
