from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class AIConfig:
    """
    Provider-agnostic configuration for AI integrations.
    """

    provider: str
    model: str

    api_key: str | None = None
    base_url: str | None = None

    temperature: float = 0.2
    max_tokens: int | None = None

    timeout: int = 60

    organization: str | None = None

    headers: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        provider = self.provider.strip().lower()
        model = self.model.strip()

        object.__setattr__(self, "provider", provider)
        object.__setattr__(self, "model", model)
        object.__setattr__(self, "api_key", _blank_to_none(self.api_key))
        object.__setattr__(self, "base_url", _blank_to_none(self.base_url))
        object.__setattr__(self, "organization", _blank_to_none(self.organization))
        object.__setattr__(self, "headers", dict(self.headers))

        if not provider:
            raise ValueError("Provider cannot be empty.")

        if not model:
            raise ValueError("Model cannot be empty.")

        if not 0.0 <= self.temperature <= 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0.")

        if self.max_tokens is not None and self.max_tokens <= 0:
            raise ValueError("max_tokens must be greater than zero.")

        if self.timeout <= 0:
            raise ValueError("timeout must be greater than zero.")

    @classmethod
    def from_mapping(
        cls,
        values: Mapping[str, Any],
    ) -> AIConfig:
        """
        Build AI configuration from a flat mapping or an ``ai`` section.
        """

        if not isinstance(values, Mapping):
            raise ValueError("AI configuration must be a mapping.")

        source = values.get("ai", values)

        if not isinstance(source, Mapping):
            raise ValueError("AI configuration must be a mapping.")

        provider = _required_str(source, "provider")
        model = _required_str(source, "model")
        timeout = _optional_int(source, "timeout", default=60)

        if timeout is None:
            raise ValueError("timeout is required.")

        return cls(
            provider=provider,
            model=model,
            api_key=_optional_str(source, "api_key"),
            base_url=_optional_str(source, "base_url"),
            temperature=_optional_float(source, "temperature", default=0.2),
            max_tokens=_optional_int(source, "max_tokens"),
            timeout=timeout,
            organization=_optional_str(source, "organization"),
            headers=_optional_headers(source),
        )

    @classmethod
    def from_env(
        cls,
        prefix: str = "PYRESTKIT_AI_",
    ) -> AIConfig:
        """
        Build AI configuration from environment variables.

        Expected variables:

        - PYRESTKIT_AI_PROVIDER
        - PYRESTKIT_AI_MODEL
        - PYRESTKIT_AI_API_KEY
        - PYRESTKIT_AI_BASE_URL
        - PYRESTKIT_AI_TEMPERATURE
        - PYRESTKIT_AI_MAX_TOKENS
        - PYRESTKIT_AI_TIMEOUT
        - PYRESTKIT_AI_ORGANIZATION
        """

        model = os.getenv(f"{prefix}MODEL")

        if model is None:
            raise ValueError(f"{prefix}MODEL is required.")

        mapping: dict[str, Any] = {
            "provider": os.getenv(f"{prefix}PROVIDER", "openai"),
            "model": model,
            "api_key": os.getenv(f"{prefix}API_KEY"),
            "base_url": os.getenv(f"{prefix}BASE_URL"),
            "temperature": os.getenv(f"{prefix}TEMPERATURE", "0.2"),
            "max_tokens": os.getenv(f"{prefix}MAX_TOKENS"),
            "timeout": os.getenv(f"{prefix}TIMEOUT", "60"),
            "organization": os.getenv(f"{prefix}ORGANIZATION"),
        }

        return cls.from_mapping(mapping)


def _blank_to_none(value: str | None) -> str | None:
    if value is None:
        return None

    value = value.strip()
    return value or None


def _required_str(
    values: Mapping[str, Any],
    key: str,
) -> str:
    value = values.get(key)

    if value is None:
        raise ValueError(f"{key} is required.")

    return str(value)


def _optional_str(
    values: Mapping[str, Any],
    key: str,
) -> str | None:
    value = values.get(key)

    if value is None:
        return None

    return str(value)


def _optional_float(
    values: Mapping[str, Any],
    key: str,
    default: float,
) -> float:
    value = values.get(key, default)

    if value is None or value == "":
        return default

    return float(value)


def _optional_int(
    values: Mapping[str, Any],
    key: str,
    default: int | None = None,
) -> int | None:
    value = values.get(key, default)

    if value is None or value == "":
        return default

    return int(value)


def _optional_headers(
    values: Mapping[str, Any],
) -> Mapping[str, str]:
    headers = values.get("headers", {})

    if headers is None:
        return {}

    if not isinstance(headers, Mapping):
        raise ValueError("headers must be a mapping.")

    return {str(key): str(value) for key, value in headers.items()}
