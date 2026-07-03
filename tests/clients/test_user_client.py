from typing import Any

from src.clients.user_client import UserClient
from src.models.request.create_user_request import CreateUserRequest
from src.models.request.update_user_request import UpdateUserRequest


def test_get_user(
    user_client: UserClient,
    requests_mock: Any,
) -> None:
    requests_mock.get(
        "https://reqres.in/api/users/2",
        json={
            "id": 2,
            "first_name": "Janet",
            "last_name": "Weaver",
        },
        status_code=200,
    )

    response = user_client.get_user(user_id=2)

    assert response.status_code == 200
    assert response.json()["id"] == 2
    assert response.json()["first_name"] == "Janet"
    assert response.json()["last_name"] == "Weaver"


def test_list_users(
    user_client: UserClient,
    requests_mock: Any,
) -> None:
    requests_mock.get(
        "https://reqres.in/api/users",
        json={
            "page": 1,
            "per_page": 6,
            "total": 12,
            "total_pages": 2,
            "data": [
                {
                    "id": 1,
                    "first_name": "George",
                    "last_name": "Bluth",
                },
                {
                    "id": 2,
                    "first_name": "Janet",
                    "last_name": "Weaver",
                },
            ],
        },
        status_code=200,
    )

    response = user_client.list_users()

    assert response.status_code == 200

    body = response.json()

    assert body["page"] == 1
    assert body["per_page"] == 6
    assert len(body["data"]) == 2
    assert body["data"][0]["id"] == 1
    assert body["data"][1]["id"] == 2


def test_create_user(
    user_client: UserClient,
    requests_mock: Any,
) -> None:
    request = CreateUserRequest(
        name="Raushan",
        job="SDET",
    )

    requests_mock.post(
        "https://reqres.in/api/users",
        json={
            "id": "101",
            "name": "Raushan",
            "job": "SDET",
            "createdAt": "2026-07-02T10:00:00Z",
        },
        status_code=201,
    )

    response = user_client.create_user(request)

    assert response.status_code == 201

    body = response.json()

    assert body["id"] == "101"
    assert body["name"] == "Raushan"
    assert body["job"] == "SDET"
    assert "createdAt" in body


def test_update_user(
    user_client: UserClient,
    requests_mock: Any,
) -> None:
    request = UpdateUserRequest(
        job="Senior SDET",
    )

    requests_mock.put(
        "https://reqres.in/api/users/2",
        json={
            "job": "Senior SDET",
            "updatedAt": "2026-07-02T10:10:00Z",
        },
        status_code=200,
    )

    response = user_client.update_user(
        user_id=2,
        request=request,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["job"] == "Senior SDET"
    assert "updatedAt" in body


def test_delete_user(
    user_client: UserClient,
    requests_mock: Any,
) -> None:
    requests_mock.delete(
        "https://reqres.in/api/users/2",
        status_code=204,
    )

    response = user_client.delete_user(user_id=2)

    assert response.status_code == 204
