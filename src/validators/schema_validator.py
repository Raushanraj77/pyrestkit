from __future__ import annotations

import json
from pathlib import Path

import requests
from jsonschema import validate

ROOT = Path(__file__).resolve().parents[2]


class SchemaValidator:
    """
    Validates API response against JSON Schema.
    """

    @staticmethod
    def validate(
        response: requests.Response,
        schema_file: str,
    ) -> None:
        schema_path = ROOT / schema_file

        with schema_path.open(
            encoding="utf-8",
        ) as file:
            schema = json.load(file)

        validate(
            instance=response.json(),
            schema=schema,
        )
