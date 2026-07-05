from __future__ import annotations

import pytest

from pyrestkit.exceptions.serialization_exception import SerializationException
from pyrestkit.serializers.response_mapper import ResponseMapper


class SampleModel:
    @classmethod
    def from_dict(cls, data: dict) -> SampleModel:
        return cls()


class FailingModel:
    @classmethod
    def from_dict(cls, data: dict) -> FailingModel:
        raise ValueError("boom")


def test_response_mapper_maps_model() -> None:
    result = ResponseMapper.map({}, SampleModel)

    assert isinstance(result, SampleModel)


def test_response_mapper_wraps_mapping_errors() -> None:
    with pytest.raises(SerializationException, match="Unable to map response"):
        ResponseMapper.map({}, FailingModel)
