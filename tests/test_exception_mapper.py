from __future__ import annotations

import pytest
import requests

from pyrestkit.exceptions.authentication_exception import AuthenticationException
from pyrestkit.exceptions.exception_mapper import ExceptionMapper
from pyrestkit.exceptions.response_exception import ResponseException
from pyrestkit.exceptions.validation_exception import ValidationException


def test_exception_mapper_returns_for_success_status() -> None:
    response = requests.Response()
    response.status_code = 200

    ExceptionMapper.raise_for_response(response)


def test_exception_mapper_maps_authentication_error() -> None:
    response = requests.Response()
    response.status_code = 401

    with pytest.raises(AuthenticationException):
        ExceptionMapper.raise_for_response(response)


def test_exception_mapper_maps_validation_error() -> None:
    response = requests.Response()
    response.status_code = 422

    with pytest.raises(ValidationException):
        ExceptionMapper.raise_for_response(response)


def test_exception_mapper_maps_generic_response_error() -> None:
    response = requests.Response()
    response.status_code = 503

    with pytest.raises(ResponseException):
        ExceptionMapper.raise_for_response(response)
