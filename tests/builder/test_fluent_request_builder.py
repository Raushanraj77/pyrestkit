from __future__ import annotations

import pytest
import requests_mock

from pyrestkit.builder.fluent_request_builder import FluentRequestBuilder
from pyrestkit.core.api_client import APIClient


def test_get_request(
    requests_mock: requests_mock.Mocker,
    api_client: APIClient,
) -> None:
    requests_mock.get(
        "https://reqres.in/api/users",
        json={"page": 1},
        status_code=200,
    )

    response = api_client.request().get("/users").send()

    assert response.status_code == 200
    assert response.json()["page"] == 1


def test_post_request(
    requests_mock: requests_mock.Mocker,
    api_client: APIClient,
) -> None:
    requests_mock.post(
        "https://reqres.in/api/users",
        json={
            "id": "100",
            "name": "John",
        },
        status_code=201,
    )

    response = api_client.request().post("/users").json({"name": "John"}).send()

    assert response.status_code == 201
    assert response.json()["name"] == "John"


def test_query_parameters(
    requests_mock: requests_mock.Mocker,
    api_client: APIClient,
) -> None:
    matcher = requests_mock.get(
        "https://reqres.in/api/users",
        json={"page": 2},
        status_code=200,
    )

    response = api_client.request().get("/users").query(page=2).send()

    assert response.status_code == 200
    assert matcher.last_request is not None
    assert matcher.last_request.qs["page"] == ["2"]
    # assert matcher.last_request.qs["page"] == ["2"]


def test_custom_header(
    requests_mock: requests_mock.Mocker,
    api_client: APIClient,
) -> None:
    matcher = requests_mock.get(
        "https://reqres.in/api/users",
        json={},
        status_code=200,
    )

    (
        api_client.request()
        .get("/users")
        .header(
            "X-Test",
            "demo",
        )
        .send()
    )

    assert matcher.last_request is not None
    assert matcher.last_request.headers["X-Test"] == "demo"


def test_multiple_headers(
    requests_mock: requests_mock.Mocker,
    api_client: APIClient,
) -> None:
    matcher = requests_mock.get(
        "https://reqres.in/api/users",
        json={},
        status_code=200,
    )

    (
        api_client.request()
        .get("/users")
        .headers(
            {
                "X-One": "1",
                "X-Two": "2",
            },
        )
        .send()
    )

    assert matcher.last_request is not None
    assert matcher.last_request.headers["X-One"] == "1"
    assert matcher.last_request.headers["X-Two"] == "2"


def test_timeout(
    requests_mock: requests_mock.Mocker,
    api_client: APIClient,
) -> None:
    requests_mock.get(
        "https://reqres.in/api/users",
        json={},
        status_code=200,
    )

    response = api_client.request().get("/users").timeout(5).send()

    assert response.status_code == 200


def test_invalid_method(
    api_client: APIClient,
) -> None:
    builder = FluentRequestBuilder(api_client)

    with pytest.raises(ValueError):
        builder.send()
