# from dataclasses import dataclass


# @dataclass(slots=True)
# class CreateUserResponse:
#     id: str
#     name: str
#     job: str
#     created_at: str

#     @classmethod
#     def from_dict(cls, data: dict) -> "CreateUserResponse":
#         return cls(
#             id=data["id"],
#             name=data["name"],
#             job=data["job"],
#             created_at=data["createdAt"],
#         )

from dataclasses import dataclass

from src.models.base_response import BaseResponse


@dataclass(slots=True)
class CreateUserResponse(BaseResponse): ...
