from typing import Type, TypeVar

T = TypeVar("T")


class ResponseMapper:

    @staticmethod
    def map(
        data: dict,
        model: Type[T],
    ) -> T:
        return model.from_dict(data)