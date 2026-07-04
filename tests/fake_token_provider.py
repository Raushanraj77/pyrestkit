from pyrestkit.auth.token_provider import TokenProvider
from pyrestkit.auth.token_response import TokenResponse


###NOT REQUIRED THIS FILE IS ONLY FOR TESTING PURPOSES. DO NOT USE IN PRODUCTION###
class FakeTokenProvider(TokenProvider):
    def __init__(self) -> None:
        self.call_count = 0

    def get_token(self) -> TokenResponse:
        self.call_count += 1

        return TokenResponse(
            access_token="fake-token",
            expires_in=3600,
        )
