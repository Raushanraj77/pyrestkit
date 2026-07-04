from __future__ import annotations

import pytest
import requests

from pyrestkit.models.response.user_response import UserResponse
from pyrestkit.response.framework_response import FrameworkResponse


def test_as_model() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "id": 2,
        "email": "janet@example.com",
        "first_name": "Janet",
        "last_name": "Weaver",
        "avatar": "https://reqres.in/img/faces/2-image.jpg"
    }
    """

    user = FrameworkResponse(response).as_model(
        UserResponse,
    )

    assert user.id == 2
    assert user.email == "janet@example.com"


# invalid model
class Dummy:
    pass


def test_as_model_invalid() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b'{"id":1}'

    with pytest.raises(TypeError):
        FrameworkResponse(response).as_model(Dummy)
