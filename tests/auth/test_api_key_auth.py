from src.auth.strategies.api_key_auth import ApiKeyAuth


def test_api_key_headers() -> None:
    auth = ApiKeyAuth("123456")

    assert auth.get_headers() == {
        "x-api-key": "123456",
    }
