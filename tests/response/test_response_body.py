from __future__ import annotations

import pytest

from pyrestkit.response.response_body import ResponseBody


def test_attribute_access() -> None:
    body = ResponseBody(
        {
            "id": 2,
            "first_name": "Janet",
        },
    )

    assert body.id == 2
    assert body.first_name == "Janet"


def test_nested_access() -> None:
    body = ResponseBody(
        {
            "data": {
                "email": "janet@example.com",
            },
        },
    )

    assert body.data.email == "janet@example.com"


def test_list_access() -> None:
    body = ResponseBody(
        {
            "users": [
                {
                    "id": 1,
                },
                {
                    "id": 2,
                },
            ],
        },
    )

    assert body.users[0].id == 1
    assert body.users[1].id == 2


def test_missing_attribute() -> None:
    body = ResponseBody(
        {
            "id": 1,
        },
    )

    with pytest.raises(AttributeError):
        _ = body.email


def test_iteration() -> None:
    body = ResponseBody(
        [
            {"id": 1},
            {"id": 2},
        ],
    )

    ids = [item.id for item in body]

    assert ids == [1, 2]


def test_response_body_get_supports_nested_paths() -> None:
    body = ResponseBody({"data": {"user": {"name": "Ada"}}})

    assert body.get("data.user.name") == "Ada"


def test_response_body_get_raises_for_missing_path() -> None:
    body = ResponseBody({"data": {"user": {"name": "Ada"}}})

    with pytest.raises(AttributeError, match="Field 'data.user.email' not found"):
        body.get("data.user.email")
