from __future__ import annotations

import pytest
import requests

from pyrestkit.assertions.assertion_exception import AssertionException
from pyrestkit.response.framework_response import FrameworkResponse


def test_have_json_count() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "data": [
            {"id": 1},
            {"id": 2},
            {"id": 3}
        ]
    }
    """

    FrameworkResponse(response).should.have_json_count(
        "data",
        3,
    )


# Wrong count
def test_have_json_count_failure() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "data": [
            {"id": 1},
            {"id": 2}
        ]
    }
    """

    with pytest.raises(AssertionException):
        FrameworkResponse(response).should.have_json_count(
            "data",
            5,
        )


# Not a list
def test_have_json_count_not_array() -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "data": {
            "id": 1
        }
    }
    """

    with pytest.raises(AssertionException):
        FrameworkResponse(response).should.have_json_count(
            "data",
            1,
        )
