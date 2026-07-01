from src.config.config import ConfigManager
from src.core.api_client import APIClient
from src.core.session_manager import SessionManager


def test_get_request(requests_mock):
    config = ConfigManager("dev")
    session_manager = SessionManager()

    client = APIClient(config, session_manager)

    requests_mock.get(
        "https://reqres.in/api/users/2",
        json={"id": 2, "first_name": "Janet"},
        status_code=200,
    )

    response = client.get("/users/2")

    assert response.status_code == 200
    assert response.json()["id"] == 2

    session_manager.close()