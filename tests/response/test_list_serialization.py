from __future__ import annotations

import pytest
import requests

from src.models.response.user_response import UserResponse
from src.response.framework_response import FrameworkResponse


def test_as_list() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    [
        {
            "id": 1,
            "email": "one@test.com",
            "first_name": "One",
            "last_name": "User",
            "avatar": ""
        },
        {
            "id": 2,
            "email": "two@test.com",
            "first_name": "Two",
            "last_name": "User",
            "avatar": ""
        }
    ]
    """

    users = FrameworkResponse(response).as_list(
        UserResponse,
    )

    assert len(users) == 2
    assert users[0].email == "one@test.com"
    assert users[1].id == 2


## invalid response
def test_as_list_invalid_json() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "id": 1
    }
    """

    with pytest.raises(TypeError):
        FrameworkResponse(response).as_list(
            UserResponse,
        )
