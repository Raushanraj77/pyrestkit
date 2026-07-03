from src.factories.user_factory import UserFactory


def test_random_factory() -> None:
    user = UserFactory.random()

    assert user.name.startswith("User-")
    assert user.job == "QA Engineer"


def test_admin_factory() -> None:
    user = UserFactory.admin()

    assert user.name == "Admin User"
    assert user.job == "Administrator"


def test_load_from_file() -> None:
    user = UserFactory.from_file("user.json")

    assert user.name == "John Doe"
    assert user.job == "Software Engineer"
