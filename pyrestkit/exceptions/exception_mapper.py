from __future__ import annotations

import requests

from pyrestkit.exceptions.authentication_exception import AuthenticationException
from pyrestkit.exceptions.response_exception import ResponseException
from pyrestkit.exceptions.validation_exception import ValidationException


class ExceptionMapper:
    """
    Maps HTTP status codes to framework exceptions.
    """

    @staticmethod
    def raise_for_response(
        response: requests.Response,
    ) -> None:
        status = response.status_code

        if status < 400:
            return

        if status == 401:
            raise AuthenticationException("Authentication failed.")

        if status == 422:
            raise ValidationException("Validation failed.")

        raise ResponseException(
            f"Request failed with status code {status}.",
        )
