from pyrestkit.endpoints.user_endpoints import UserEndpoints


def test_list_users_endpoint() -> None:
    assert UserEndpoints.list_users() == "/users"


def test_create_user_endpoint() -> None:
    assert UserEndpoints.create_user() == "/users"


def test_get_user_endpoint() -> None:
    assert UserEndpoints.get_user(user_id=10) == "/users/10"


def test_update_user_endpoint() -> None:
    assert UserEndpoints.update_user(user_id=25) == "/users/25"


def test_delete_user_endpoint() -> None:
    assert UserEndpoints.delete_user(user_id=99) == "/users/99"
