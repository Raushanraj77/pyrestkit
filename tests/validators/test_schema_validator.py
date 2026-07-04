from __future__ import annotations

import requests_mock

from pyrestkit.core.api_client import APIClient
from pyrestkit.validators.schema_validator import SchemaValidator


def test_schema_validator(
    requests_mock: requests_mock.Mocker,
    api_client: APIClient,
) -> None:
    requests_mock.get(
        "https://reqres.in/api/users/2",
        json={
            "id": 2,
            "email": "janet@example.com",
            "first_name": "Janet",
            "last_name": "Weaver",
        },
        status_code=200,
    )

    response = api_client.get("/users/2")

    SchemaValidator.validate(
        response,
        "schemas/get_user.json",
    )
