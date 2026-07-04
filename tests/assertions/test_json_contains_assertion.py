from __future__ import annotations

import pytest
import requests

from src.assertions.assertion_exception import AssertionException
from src.response.framework_response import FrameworkResponse


# Success (string)
def test_have_json_contains_string() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "roles": [
            "user",
            "admin"
        ]
    }
    """

    FrameworkResponse(response).should.have_json_contains(
        "roles",
        "admin",
    )


# Success (object)


def test_have_json_contains_object() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "data": [
            {
                "id": 1
            },
            {
                "id": 2
            }
        ]
    }
    """

    FrameworkResponse(response).should.have_json_contains(
        "data",
        {"id": 2},
    )


# Failure
def test_have_json_contains_failure() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "roles": [
            "user"
        ]
    }
    """

    with pytest.raises(AssertionException):
        FrameworkResponse(response).should.have_json_contains(
            "roles",
            "admin",
        )


# Not a list
def test_have_json_contains_not_list() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "roles": {
            "name": "admin"
        }
    }
    """

    with pytest.raises(AssertionException):
        FrameworkResponse(response).should.have_json_contains(
            "roles",
            "admin",
        )
