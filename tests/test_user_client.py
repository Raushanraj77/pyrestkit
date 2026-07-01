from src.clients.user_client import UserClient
from src.config.config import ConfigManager
from src.core.api_client import APIClient
from src.core.session_manager import SessionManager


def test_get_user(requests_mock):
    config = ConfigManager("dev")
    session_manager = SessionManager()

    api_client = APIClient(config, session_manager)
    user_client = UserClient(api_client)

    requests_mock.get(
        "https://reqres.in/api/users/2",
        json={
            "id": 2,
            "first_name": "Janet",
            "last_name": "Weaver"
        },
        status_code=200,
    )

    response = user_client.get_user(user_id=2)

    assert response.status_code == 200
    assert response.json()["id"] == 2

    session_manager.close()


def test_list_users(requests_mock):
    config = ConfigManager("dev")
    session_manager = SessionManager()

    api_client = APIClient(config, session_manager)
    user_client = UserClient(api_client)

    requests_mock.get(
        "https://reqres.in/api/users",
        json={
            "page": 1,
            "data": []
        },
        status_code=200,
    )

    response = user_client.list_users()

    assert response.status_code == 200

    session_manager.close()


def test_create_user(requests_mock):
    config = ConfigManager("dev")
    session_manager = SessionManager()

    api_client = APIClient(config, session_manager)
    user_client = UserClient(api_client)

    payload = {
        "name": "Raushan",
        "job": "SDET"
    }

    requests_mock.post(
        "https://reqres.in/api/users",
        json={
            "id": "101",
            "name": "Raushan",
            "job": "SDET"
        },
        status_code=201,
    )

    response = user_client.create_user(payload)

    assert response.status_code == 201
    assert response.json()["name"] == "Raushan"

    session_manager.close()


def test_update_user(requests_mock):
    config = ConfigManager("dev")
    session_manager = SessionManager()

    api_client = APIClient(config, session_manager)
    user_client = UserClient(api_client)

    payload = {
        "job": "Senior SDET"
    }

    requests_mock.put(
        "https://reqres.in/api/users/2",
        json=payload,
        status_code=200,
    )

    response = user_client.update_user(
        user_id=2,
        payload=payload,
    )

    assert response.status_code == 200

    session_manager.close()


def test_delete_user(requests_mock):
    config = ConfigManager("dev")
    session_manager = SessionManager()

    api_client = APIClient(config, session_manager)
    user_client = UserClient(api_client)

    requests_mock.delete(
        "https://reqres.in/api/users/2",
        status_code=204,
    )

    response = user_client.delete_user(user_id=2)

    assert response.status_code == 204

    session_manager.close()