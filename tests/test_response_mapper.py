from src.mapper.response_mapper import ResponseMapper
from src.models.response.get_user_response import GetUserResponse


def test_response_mapper():

    data = {
        "id": 2,
        "email": "janet@reqres.in",
        "first_name": "Janet",
        "last_name": "Weaver",
        "avatar": "avatar-url",
    }

    user = ResponseMapper.map(
        data,
        GetUserResponse,
    )

    assert user.id == 2
    assert user.first_name == "Janet"