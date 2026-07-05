from __future__ import annotations

from typing import Any

import pytest

from pyrestkit.ai.config import AIConfig
from pyrestkit.ai.exceptions import AIConfigurationError, AIProviderError
from pyrestkit.ai.providers.openai import OpenAIResponsesProvider


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


def test_openai_provider_calls_responses_api() -> None:
    session = FakeSession(
        FakeResponse({
            "output_text": "Root cause found.",
        })
    )
    provider = OpenAIResponsesProvider(session=session)
    config = AIConfig(
        provider="openai",
        model="gpt-test",
        api_key="key",
        max_tokens=200,
        organization="org",
    )

    result = provider.complete(
        "Analyze",
        config=config,
        system_prompt="You are a tester.",
    )

    assert result == "Root cause found."
    assert session.url == "https://api.openai.com/v1/responses"
    assert session.payload == {
        "model": "gpt-test",
        "input": "Analyze",
        "temperature": 0.2,
        "instructions": "You are a tester.",
        "max_output_tokens": 200,
    }
    assert session.headers["Authorization"] == "Bearer key"
    assert session.headers["OpenAI-Organization"] == "org"
    assert session.timeout == 60


def test_openai_provider_extracts_nested_output_text() -> None:
    session = FakeSession(
        FakeResponse({
            "output": [
                {
                    "content": [
                        {
                            "type": "output_text",
                            "text": "Nested text",
                        }
                    ]
                }
            ]
        })
    )
    provider = OpenAIResponsesProvider(session=session)
    config = AIConfig(
        provider="openai",
        model="gpt-test",
        api_key="key",
    )

    assert provider.complete("Analyze", config=config) == "Nested text"


def test_openai_provider_requires_api_key() -> None:
    provider = OpenAIResponsesProvider(session=FakeSession(FakeResponse({})))
    config = AIConfig(
        provider="openai",
        model="gpt-test",
    )

    with pytest.raises(AIConfigurationError, match="API key"):
        provider.complete("Analyze", config=config)


def test_openai_provider_raises_on_http_error() -> None:
    session = FakeSession(
        FakeResponse(
            {},
            status_code=429,
            text="rate limited",
        )
    )
    provider = OpenAIResponsesProvider(session=session)
    config = AIConfig(
        provider="openai",
        model="gpt-test",
        api_key="key",
    )

    with pytest.raises(AIProviderError, match="429"):
        provider.complete("Analyze", config=config)
