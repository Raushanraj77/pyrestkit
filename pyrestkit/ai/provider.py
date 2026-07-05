from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from pyrestkit.ai.config import AIConfig


class AIProvider(Protocol):
    """
    Contract implemented by concrete AI providers.
    """

    def complete(
        self,
        prompt: str,
        *,
        config: AIConfig,
        system_prompt: str | None = None,
    ) -> str:
        """
        Return a text completion for the given prompt.
        """
        ...


@dataclass(frozen=True, slots=True)
class AIProviderCall:
    prompt: str
    system_prompt: str | None
    config: AIConfig


@dataclass(slots=True)
class StaticAIProvider:
    """
    Deterministic provider for tests and offline demos.
    """

    response: str
    calls: list[AIProviderCall] = field(default_factory=list)

    def complete(
        self,
        prompt: str,
        *,
        config: AIConfig,
        system_prompt: str | None = None,
    ) -> str:
        self.calls.append(
            AIProviderCall(
                prompt=prompt,
                system_prompt=system_prompt,
                config=config,
            )
        )

        return self.response
