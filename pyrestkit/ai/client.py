from __future__ import annotations

from collections.abc import Callable

from pyrestkit.ai.config import AIConfig
from pyrestkit.ai.exceptions import AIConfigurationError
from pyrestkit.ai.provider import AIProvider
from pyrestkit.ai.providers import (
    AnthropicProvider,
    AzureOpenAIProvider,
    BedrockProvider,
    CohereProvider,
    GeminiProvider,
    GroqProvider,
    MistralProvider,
    OllamaProvider,
    OpenAIResponsesProvider,
)

ProviderFactory = Callable[[], AIProvider]

_PROVIDER_FACTORIES: dict[str, ProviderFactory] = {
    "openai": OpenAIResponsesProvider,
    "ollama": OllamaProvider,
    "anthropic": AnthropicProvider,
    "gemini": GeminiProvider,
    "azure-openai": AzureOpenAIProvider,
    "azure_openai": AzureOpenAIProvider,
    "cohere": CohereProvider,
    "mistral": MistralProvider,
    "groq": GroqProvider,
    "bedrock": BedrockProvider,
}


class AIClient:
    """
    Small facade that keeps framework code independent from provider details.
    """

    def __init__(
        self,
        config: AIConfig,
        provider: AIProvider | None = None,
    ) -> None:
        self._config = config
        self._provider = provider or create_provider(config.provider)

    @property
    def config(self) -> AIConfig:
        return self._config

    def complete(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
    ) -> str:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        return self._provider.complete(
            prompt,
            config=self._config,
            system_prompt=system_prompt,
        )


def create_provider(
    provider_name: str,
) -> AIProvider:
    provider = provider_name.strip().lower()

    if not provider:
        raise AIConfigurationError("AI provider name cannot be empty.")

    factory = _PROVIDER_FACTORIES.get(provider)

    if factory is None:
        raise AIConfigurationError(
            f"No AI provider registered for '{provider_name}'. "
            "Install the provider package or register a custom provider."
        )

    return factory()


def register_provider(
    provider_name: str,
    factory: ProviderFactory,
) -> None:
    provider = provider_name.strip().lower()

    if not provider:
        raise AIConfigurationError("AI provider name cannot be empty.")

    _PROVIDER_FACTORIES[provider] = factory


def available_providers() -> tuple[str, ...]:
    return tuple(sorted(_PROVIDER_FACTORIES))
