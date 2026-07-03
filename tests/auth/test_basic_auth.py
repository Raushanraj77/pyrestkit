from src.auth.strategies.basic_auth import BasicAuth


def test_basic_auth_headers() -> None:
    auth = BasicAuth(
        username="admin",
        password="password",
    )

    headers = auth.get_headers()

    assert "Authorization" in headers
    assert headers["Authorization"].startswith("Basic ")
