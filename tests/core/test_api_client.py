from typing import Any

from pyrestkit.core.api_client import APIClient


def test_get_request(
    api_client: APIClient,
    requests_mock: Any,
) -> None:
    requests_mock.get(
        "https://reqres.in/api/users/2",
        json={
            "id": 2,
            "first_name": "Janet",
        },
        status_code=200,
    )

    response = api_client.get("/users/2")

    assert response.status_code == 200
    assert response.json()["id"] == 2
