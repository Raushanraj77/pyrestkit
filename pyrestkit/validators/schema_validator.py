from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import validate

from pyrestkit.response.framework_response import FrameworkResponse


class SchemaValidator:
    """
    Validates a response against a JSON schema.
    """

    @staticmethod
    def validate(
        response: FrameworkResponse,
        schema_path: str,
    ) -> None:
        schema_file = Path(schema_path)

        with schema_file.open(
            encoding="utf-8",
        ) as file:
            schema: dict[str, Any] = json.load(file)

        validate(
            # instance=response.json(),
            instance=response.body.to_dict(),
            schema=schema,
        )
