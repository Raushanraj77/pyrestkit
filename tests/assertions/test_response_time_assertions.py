from __future__ import annotations

from datetime import timedelta

import pytest
import requests

from pyrestkit.assertions.assertion_exception import AssertionException
from pyrestkit.response.framework_response import FrameworkResponse


def test_response_within_limit() -> None:
    response = requests.Response()

    response.status_code = 200
    response.elapsed = timedelta(milliseconds=250)

    FrameworkResponse(response).should.respond_within(500)


def test_response_exceeds_limit() -> None:
    response = requests.Response()

    response.status_code = 200
    response.elapsed = timedelta(milliseconds=900)

    with pytest.raises(AssertionException):
        FrameworkResponse(response).should.respond_within(500)
