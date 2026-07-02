from dataclasses import dataclass


@dataclass(slots=True)
class CreateUserRequest:
    """
    Request model for creating a user.
    """

    name: str
    job: str