from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast


class BaseFactory:
    """
    Base class for loading test data.
    """

    TESTDATA_DIR = Path("testdata")

    @classmethod
    def load_json(
        cls,
        filename: str,
    ) -> dict[str, Any]:
        file_path = cls.TESTDATA_DIR / filename

        with file_path.open(
            encoding="utf-8",
        ) as file:
            return cast(dict[str, Any], json.load(file))
