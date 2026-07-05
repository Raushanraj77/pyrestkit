from __future__ import annotations

from collections.abc import Iterator
from typing import Any


class ResponseBody:
    """
    Provides attribute-style access to JSON responses.

    Example:

        body.first_name
        body.data.email
        body.users[0].email
    """

    def __init__(
        self,
        data: Any,
    ) -> None:
        self._data = data

    def __getattr__(
        self,
        name: str,
    ) -> Any:
        if not isinstance(self._data, dict):
            raise AttributeError(
                f"'{type(self._data).__name__}' has no attribute '{name}'."
            )

        if name not in self._data:
            raise AttributeError(f"Field '{name}' not found.")

        return self._wrap(
            self._data[name],
        )

    def __getitem__(
        self,
        key: Any,
    ) -> Any:
        return self._wrap(
            self._data[key],
        )

    #     def __iter__(
    #         self,
    #     ):
    #         if isinstance(
    #             self._data,
    #             list,
    #         ):
    #             for item in self._data:
    #                 yield self._wrap(item)
    #         else:
    #             raise TypeError("ResponseBody is not iterable.")

    #     from collections.abc import Iterator

    # ...

    def __iter__(
        self,
    ) -> Iterator[Any]:
        if isinstance(
            self._data,
            list,
        ):
            for item in self._data:
                yield self._wrap(item)
        else:
            raise TypeError("ResponseBody is not iterable.")

    @staticmethod
    def _wrap(
        value: Any,
    ) -> Any:
        if isinstance(
            value,
            dict,
        ):
            return ResponseBody(value)

        if isinstance(
            value,
            list,
        ):
            return [ResponseBody._wrap(item) for item in value]

        return value

    def to_dict(
        self,
    ) -> Any:
        """
        Returns the underlying JSON object.
        """
        return self._data

    def get(
        self,
        path: str,
    ) -> Any:
        """
        Returns a JSON value using dot notation.

        Example:

            body.get("data.users")
        """

        current: Any = self._data

        for part in path.split("."):
            if isinstance(current, dict):
                if part not in current:
                    raise AttributeError(f"Field '{path}' not found.")
                current = current[part]
            else:
                raise AttributeError(f"Field '{path}' not found.")

        return current
