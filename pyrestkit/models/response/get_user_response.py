# from dataclasses import dataclass


# @dataclass(slots=True)
# class GetUserResponse:
#     id: int
#     email: str
#     first_name: str
#     last_name: str
#     avatar: str

#     @classmethod
#     def from_dict(cls, data: dict) -> "GetUserResponse":
#         return cls(
#             id=data["id"],
#             email=data["email"],
#             first_name=data["first_name"],
#             last_name=data["last_name"],
#             avatar=data["avatar"],
#         )

from dataclasses import dataclass

from pyrestkit.models.base_response import BaseResponse


@dataclass(slots=True)
class GetUserResponse(BaseResponse): ...
