from src.clients.user_client import UserClient


def test_get_user(
    user_client: UserClient,
    requests_mock,
):
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


def test_list_users(
    user_client: UserClient,
    requests_mock,
):
    requests_mock.get(
        "https://reqres.in/api/users",
        json={
            "page": 1,
            "data": [],
        },
        status_code=200,
    )

    response = user_client.list_users()

    assert response.status_code == 200
    assert response.json()["page"] == 1


def test_create_user(
    user_client: UserClient,
    requests_mock,
):
    payload = {
        "name": "Raushan",
        "job": "SDET",
    }

    requests_mock.post(
        "https://reqres.in/api/users",
        json={
            "id": "101",
            "name": "Raushan",
            "job": "SDET",
        },
        status_code=201,
    )

    response = user_client.create_user(payload)

    assert response.status_code == 201
    assert response.json()["name"] == "Raushan"
    assert response.json()["job"] == "SDET"


def test_update_user(
    user_client: UserClient,
    requests_mock,
):
    payload = {
        "job": "Senior SDET",
    }

    requests_mock.put(
        "https://reqres.in/api/users/2",
        json={
            "job": "Senior SDET",
        },
        status_code=200,
    )

    response = user_client.update_user(
        user_id=2,
        payload=payload,
    )

    assert response.status_code == 200
    assert response.json()["job"] == "Senior SDET"


def test_delete_user(
    user_client: UserClient,
    requests_mock,
):
    requests_mock.delete(
        "https://reqres.in/api/users/2",
        status_code=204,
    )

    response = user_client.delete_user(user_id=2)

    assert response.status_code == 204