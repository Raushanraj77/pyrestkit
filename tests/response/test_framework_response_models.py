from __future__ import annotations

import json
from dataclasses import dataclass

import pytest
import requests

from pyrestkit.ai.client import AIClient
from pyrestkit.ai.config import AIConfig
from pyrestkit.ai.exceptions import AIConfigurationError
from pyrestkit.ai.models import FailureAnalysis
from pyrestkit.ai.provider import StaticAIProvider
from pyrestkit.response.framework_response import FrameworkResponse


@dataclass(slots=True)
class User:
    id: int
    name: str


def test_as_model_root() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "id": 1,
        "name": "John"
    }
    """

    user = FrameworkResponse(response).as_model(User)

    assert user.id == 1
    assert user.name == "John"


def test_as_model_nested() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "data": {
            "id": 2,
            "name": "Jane"
        }
    }
    """

    user = FrameworkResponse(response).as_model(
        User,
        path="data",
    )

    assert user.id == 2
    assert user.name == "Jane"


def test_as_model_deep_nested() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "response": {
            "user": {
                "id": 3,
                "name": "Bob"
            }
        }
    }
    """

    user = FrameworkResponse(response).as_model(
        User,
        path="response.user",
    )

    assert user.id == 3
    assert user.name == "Bob"


def test_as_list_root() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    [
        {
            "id": 1,
            "name": "John"
        },
        {
            "id": 2,
            "name": "Jane"
        }
    ]
    """

    users = FrameworkResponse(response).as_list(User)

    assert len(users) == 2
    assert users[0].id == 1
    assert users[1].name == "Jane"


def test_as_list_nested() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "data": [
            {
                "id": 1,
                "name": "John"
            },
            {
                "id": 2,
                "name": "Jane"
            }
        ]
    }
    """

    users = FrameworkResponse(response).as_list(
        User,
        path="data",
    )

    assert len(users) == 2
    assert users[0].id == 1
    assert users[1].name == "Jane"


def test_as_list_deep_nested() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "response": {
            "users": [
                {
                    "id": 1,
                    "name": "John"
                },
                {
                    "id": 2,
                    "name": "Jane"
                }
            ]
        }
    }
    """

    users = FrameworkResponse(response).as_list(
        User,
        path="response.users",
    )

    assert len(users) == 2
    assert users[0].id == 1
    assert users[1].id == 2


def test_as_model_invalid_path() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "data": {
            "id": 1,
            "name": "John"
        }
    }
    """

    with pytest.raises(KeyError):
        FrameworkResponse(response).as_model(
            User,
            path="invalid",
        )


def test_as_list_invalid_path() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "users": []
    }
    """

    with pytest.raises(KeyError):
        FrameworkResponse(response).as_list(
            User,
            path="data",
        )


def test_as_model_invalid_json_type() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    [
        {
            "id": 1,
            "name": "John"
        }
    ]
    """

    with pytest.raises(TypeError):
        FrameworkResponse(response).as_model(User)


def test_as_list_invalid_json_type() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "id": 1,
        "name": "John"
    }
    """

    with pytest.raises(TypeError):
        FrameworkResponse(response).as_list(User)


def test_as_model_requires_dataclass() -> None:
    class Dummy:
        pass

    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "id": 1,
        "name": "John"
    }
    """

    with pytest.raises(TypeError):
        FrameworkResponse(response).as_model(Dummy)


def test_framework_response_ai_returns_structured_failure_analysis() -> None:
    response = requests.Response()
    response.status_code = 500
    response._content = b'{"error":"bad"}'
    response.url = "https://example.com/users/2"

    provider = StaticAIProvider(
        json.dumps({
            "summary": "Request failed",
            "likely_cause": "Server error",
            "recommended_fix": "Retry later",
            "confidence": 0.9,
        })
    )
    client = AIClient(
        config=AIConfig(provider="openai", model="gpt-test"),
        provider=provider,
    )

    analysis = FrameworkResponse(response).ai.explain_failure(client=client)

    assert isinstance(analysis, FailureAnalysis)
    assert analysis.summary == "Request failed"
    assert analysis.likely_cause == "Server error"
    assert analysis.recommended_fix == "Retry later"
    assert analysis.confidence == 0.9


def test_framework_response_ai_requires_configuration() -> None:
    response = requests.Response()
    response.status_code = 500
    response._content = b'{"error":"bad"}'

    with pytest.raises(AIConfigurationError, match="AI is not configured"):
        FrameworkResponse(response).ai.explain_failure()


def test_as_list_requires_dataclass() -> None:
    class Dummy:
        pass

    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    []
    """

    with pytest.raises(TypeError):
        FrameworkResponse(response).as_list(Dummy)
