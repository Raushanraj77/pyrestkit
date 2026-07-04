from __future__ import annotations

import pytest
import requests

from pyrestkit.assertions.assertion_exception import AssertionException
from pyrestkit.response.framework_response import FrameworkResponse


def test_have_status_passes() -> None:
    response = requests.Response()
    response.status_code = 200

    FrameworkResponse(response).should.have_status(200)


def test_have_status_fails() -> None:
    response = requests.Response()
    response.status_code = 404

    with pytest.raises(AssertionException):
        FrameworkResponse(response).should.have_status(200)


def test_be_successful() -> None:
    response = requests.Response()
    response.status_code = 200

    FrameworkResponse(response).should.be_successful()
