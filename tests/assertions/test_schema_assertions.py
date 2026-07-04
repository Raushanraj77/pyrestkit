from __future__ import annotations

import json
from pathlib import Path

import pytest
import requests
from jsonschema import ValidationError

from src.response.framework_response import FrameworkResponse


def test_match_schema(
    tmp_path: Path,
) -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "id": 1,
        "name": "John"
    }
    """

    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"},
        },
        "required": [
            "id",
            "name",
        ],
    }

    schema_file = tmp_path / "user.json"

    schema_file.write_text(
        json.dumps(schema),
        encoding="utf-8",
    )

    FrameworkResponse(response).should.match_schema(
        str(schema_file),
    )


def test_match_schema_failure(
    tmp_path: Path,
) -> None:
    response = requests.Response()

    response.status_code = 200

    response._content = b"""
    {
        "id": "abc"
    }
    """

    schema = {
        "type": "object",
        "properties": {
            "id": {
                "type": "number",
            },
        },
    }

    schema_file = tmp_path / "user.json"

    schema_file.write_text(
        json.dumps(schema),
        encoding="utf-8",
    )

    with pytest.raises(ValidationError):
        FrameworkResponse(response).should.match_schema(
            str(schema_file),
        )
