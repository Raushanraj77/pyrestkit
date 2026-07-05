import pytest
import requests

from pyrestkit.exceptions.validation_exception import ValidationException
from pyrestkit.validators.response_validator import ResponseValidator


def test_response_validator(requests_mock, api_client):

    requests_mock.get(
        "https://reqres.in/api/users/2",
        json={
            "id": 2,
        },
        status_code=200,
    )

    response = api_client.get("/users/2")

    ResponseValidator(response).status_code(200).has_key("id").field_equals("id", 2)


def test_response_validator_raises_for_status_mismatch() -> None:
    response = requests.Response()
    response.status_code = 500
    response._content = b'{"id": 2}'
    response.headers["Content-Type"] = "application/json"

    with pytest.raises(ValidationException, match="Expected status code 200"):
        ResponseValidator(response).status_code(200)


def test_response_validator_raises_for_missing_key(requests_mock, api_client):
    requests_mock.get(
        "https://reqres.in/api/users/2",
        json={"id": 2},
        status_code=200,
    )

    response = api_client.get("/users/2")

    with pytest.raises(ValidationException, match="does not contain key 'name'"):
        ResponseValidator(response).has_key("name")
