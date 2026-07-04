from __future__ import annotations

import pytest
import requests

from pyrestkit.assertions.assertion_exception import AssertionException
from pyrestkit.response.framework_response import FrameworkResponse


def test_have_json_root() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "id": 2,
        "name": "Janet"
    }
    """

    FrameworkResponse(response).should.have_json(
        "id",
        2,
    )


def test_have_json_nested() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "data": {
            "email": "janet@example.com"
        }
    }
    """

    FrameworkResponse(response).should.have_json(
        "data.email",
        "janet@example.com",
    )


def test_have_json_failure() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "id": 5
    }
    """

    with pytest.raises(AssertionException):
        FrameworkResponse(response).should.have_json(
            "id",
            10,
        )
