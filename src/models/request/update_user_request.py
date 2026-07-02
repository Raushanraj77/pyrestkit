from dataclasses import dataclass


@dataclass(slots=True)
class UpdateUserRequest:
    """
    Request model for updating a user.
    """

    job: str
