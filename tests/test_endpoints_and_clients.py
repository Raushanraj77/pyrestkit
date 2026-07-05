from __future__ import annotations

import requests

from pyrestkit.clients.base_client import BaseClient
from pyrestkit.core.api_client import APIClient
from pyrestkit.endpoints.base_endpoints import BaseEndpoints
from pyrestkit.endpoints.user_endpoints import UserEndpoints
from pyrestkit.response.framework_response import FrameworkResponse


class DummyAPIClient(APIClient):
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict]] = []

    def get(self, endpoint: str, **kwargs: dict) -> FrameworkResponse:
        self.calls.append(("GET", endpoint, kwargs))
        response = requests.Response()
        response.status_code = 200
        return FrameworkResponse(response)

    def post(self, endpoint: str, **kwargs: dict) -> FrameworkResponse:
        self.calls.append(("POST", endpoint, kwargs))
        response = requests.Response()
        response.status_code = 200
        return FrameworkResponse(response)

    def put(self, endpoint: str, **kwargs: dict) -> FrameworkResponse:
        self.calls.append(("PUT", endpoint, kwargs))
        response = requests.Response()
        response.status_code = 200
        return FrameworkResponse(response)

    def patch(self, endpoint: str, **kwargs: dict) -> FrameworkResponse:
        self.calls.append(("PATCH", endpoint, kwargs))
        response = requests.Response()
        response.status_code = 200
        return FrameworkResponse(response)

    def delete(self, endpoint: str, **kwargs: dict) -> FrameworkResponse:
        self.calls.append(("DELETE", endpoint, kwargs))
        response = requests.Response()
        response.status_code = 200
        return FrameworkResponse(response)


def test_base_endpoints_build_paths() -> None:
    assert BaseEndpoints.build("/users") == "/users"


def test_user_endpoints_build_paths() -> None:
    assert UserEndpoints.list_users() == "/users"
    assert UserEndpoints.create_user() == "/users"
    assert UserEndpoints.get_user(7) == "/users/7"
    assert UserEndpoints.update_user(7) == "/users/7"
    assert UserEndpoints.delete_user(7) == "/users/7"


def test_base_client_forwards_methods() -> None:
    client = DummyAPIClient()
    base_client = BaseClient(client)

    response = base_client.get("/users", timeout=10)
    base_client.post("/users", json={"name": "John"})
    base_client.put("/users", data={"name": "John"})
    base_client.patch("/users", headers={"X-Test": "1"})
    base_client.delete("/users")

    assert response.status_code == 200
    assert client.calls[0] == ("GET", "/users", {"timeout": 10})
