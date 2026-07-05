from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

import pytest

from pyrestkit.ai.config import AIConfig


def test_ai_config_normalizes_provider_and_model() -> None:
    config = AIConfig(
        provider="OpenAI",
        model=" gpt-test ",
        api_key=" ",
        headers={"X-Test": "1"},
    )

    assert config.provider == "openai"
    assert config.model == "gpt-test"
    assert config.api_key is None
    assert config.headers == {"X-Test": "1"}


def test_ai_config_accepts_custom_provider_name() -> None:
    config = AIConfig(
        provider="internal-llm",
        model="model",
    )

    assert config.provider == "internal-llm"


def test_ai_config_rejects_empty_provider() -> None:
    with pytest.raises(ValueError, match="Provider cannot be empty"):
        AIConfig(
            provider=" ",
            model="model",
        )


def test_ai_config_rejects_invalid_temperature() -> None:
    with pytest.raises(ValueError, match="Temperature"):
        AIConfig(
            provider="openai",
            model="model",
            temperature=3.0,
        )


def test_ai_config_rejects_invalid_max_tokens() -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        AIConfig(
            provider="openai",
            model="model",
            max_tokens=0,
        )


def test_ai_config_rejects_invalid_timeout() -> None:
    with pytest.raises(ValueError, match="timeout"):
        AIConfig(
            provider="openai",
            model="model",
            timeout=0,
        )


def test_ai_config_from_nested_mapping() -> None:
    config = AIConfig.from_mapping({
        "ai": {
            "provider": "ollama",
            "model": "llama3.2",
            "temperature": "0.1",
            "max_tokens": "500",
            "timeout": "20",
        }
    })

    assert config.provider == "ollama"
    assert config.model == "llama3.2"
    assert config.temperature == 0.1
    assert config.max_tokens == 500
    assert config.timeout == 20


def test_ai_config_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PYRESTKIT_AI_PROVIDER", "openai")
    monkeypatch.setenv("PYRESTKIT_AI_MODEL", "gpt-test")
    monkeypatch.setenv("PYRESTKIT_AI_API_KEY", "test-key")
    monkeypatch.setenv("PYRESTKIT_AI_TEMPERATURE", "0.3")

    config = AIConfig.from_env()

    assert config.provider == "openai"
    assert config.model == "gpt-test"
    assert config.api_key == "test-key"
    assert config.temperature == 0.3


def test_ai_config_from_mapping_rejects_non_mapping() -> None:
    invalid = cast(Mapping[str, Any], "not-a-mapping")

    with pytest.raises(ValueError, match="must be a mapping"):
        AIConfig.from_mapping(invalid)


def test_ai_config_from_env_requires_model(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PYRESTKIT_AI_MODEL", raising=False)

    with pytest.raises(ValueError, match="MODEL is required"):
        AIConfig.from_env()
