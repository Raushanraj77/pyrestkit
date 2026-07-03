from __future__ import annotations

from typing import Any, TypeVar, cast

from src.exceptions.serialization_exception import SerializationException

T = TypeVar("T")


class ResponseMapper:
    """
    Maps API response dictionaries to model objects.
    """

    @staticmethod
    def map(
        data: dict[str, Any],
        model: type[T],
    ) -> T:
        try:
            return cast(T, model.from_dict(data))  # type: ignore[attr-defined]
        except Exception as exc:
            raise SerializationException(
                f"Unable to map response to {model.__name__}"
            ) from exc
