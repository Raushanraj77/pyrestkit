from src.auth.bearer_auth import BearerAuth


def test_bearer_auth_headers() -> None:
    auth = BearerAuth("my-token")

    assert auth.get_headers() == {
        "Authorization": "Bearer my-token",
    }
