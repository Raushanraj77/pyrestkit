from requests_mock import Mocker

from src.core.api_client import APIClient
from src.validators.schema_validator import SchemaValidator

RequestsMock = Mocker


def test_schema_validator(
    requests_mock: RequestsMock,
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
