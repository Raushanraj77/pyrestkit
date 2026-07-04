from unittest.mock import Mock

import pytest
import requests
from requests.exceptions import ConnectionError

from pyrestkit.retry.retry_handler import RetryHandler
from pyrestkit.retry.retry_policy import RetryPolicy


def test_returns_success_without_retry() -> None:
    response = Mock(spec=requests.Response)
    response.status_code = 200

    request = Mock(return_value=response)

    handler = RetryHandler(RetryPolicy())

    result = handler.execute(request)

    assert result.status_code == 200
    assert request.call_count == 1


def test_retries_until_success(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "pyrestkit.retry.backoff.time.sleep",
        lambda _: None,
    )

    failure = Mock(spec=requests.Response)
    failure.status_code = 500

    success = Mock(spec=requests.Response)
    success.status_code = 200

    request = Mock(
        side_effect=[
            failure,
            failure,
            success,
        ],
    )

    handler = RetryHandler(RetryPolicy())

    result = handler.execute(request)

    assert result.status_code == 200
    assert request.call_count == 3


def test_retries_exception_then_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "pyrestkit.retry.backoff.time.sleep",
        lambda _: None,
    )

    response = Mock(spec=requests.Response)
    response.status_code = 200

    request = Mock(
        side_effect=[
            ConnectionError(),
            response,
        ],
    )

    handler = RetryHandler(RetryPolicy())

    result = handler.execute(request)

    assert result.status_code == 200
    assert request.call_count == 2


def test_raises_after_retry_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "pyrestkit.retry.backoff.time.sleep",
        lambda _: None,
    )

    request = Mock(
        side_effect=ConnectionError(),
    )

    handler = RetryHandler(RetryPolicy(retries=3))

    with pytest.raises(ConnectionError):
        handler.execute(request)

    assert request.call_count == 3
