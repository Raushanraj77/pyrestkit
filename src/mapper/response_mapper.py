from typing import Any, TypeVar

from src.models.base_response import BaseResponse

T = TypeVar("T", bound=BaseResponse)


class ResponseMapper:
    @staticmethod
    def map(
        data: dict[str, Any],
        model: type[T],
    ) -> T:
        return model.from_dict(data)
