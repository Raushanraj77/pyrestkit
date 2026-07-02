from src.validators.response_validator import ResponseValidator


def test_response_validator(requests_mock, api_client):

    requests_mock.get(
        "https://reqres.in/api/users/2",
        json={
            "id": 2,
        },
        status_code=200,
    )

    response = api_client.get("/users/2")

    ResponseValidator(response).status_code(200).has_key("id").field_equals("id", 2)
