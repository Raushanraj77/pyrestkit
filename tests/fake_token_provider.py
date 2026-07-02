from src.auth.token_provider import TokenProvider


class FakeTokenProvider(TokenProvider):
    def get_token(self) -> str:
        return "fake-token"
