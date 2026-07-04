from __future__ import annotations

from dataclasses import dataclass

import pytest
import requests

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
