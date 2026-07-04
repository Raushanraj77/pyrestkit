from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from pyrestkit.exceptions.configuration_exception import ConfigurationException


class ConfigManager:
    """
    Loads environment configuration from JSON files.

    Why Path(__file__).parent?

    Path(__file__).parent locates the directory containing
    config.py and appends the selected environment JSON
    file. This keeps the implementation portable across
    operating systems.

    Why use @property?

    It allows callers to access configuration values like
    attributes while keeping the flexibility to validate or
    compute values internally in the future.

    Why validate the file?

    If a user runs:

        pytest --env=production

    and production.json does not exist, the framework fails
    immediately with a clear error message.
    """

    def __init__(
        self,
        environment: str = "dev",
    ) -> None:
        self.environment = environment.lower()

        config_file = Path(__file__).parent / f"{self.environment}.json"

        if not config_file.exists():
            raise ConfigurationException(
                f"Configuration file '{self.environment}' not found.",
            )

        with config_file.open(
            encoding="utf-8",
        ) as file:
            self.config: dict[str, Any] = json.load(file)

    @property
    def base_url(self) -> str:
        return cast(
            str,
            self.config["base_url"],
        )

    @property
    def timeout(self) -> int:
        return cast(
            int,
            self.config.get(
                "timeout",
                30,
            ),
        )

    @property
    def headers(self) -> dict[str, str]:
        return cast(
            dict[str, str],
            self.config.get(
                "headers",
                {},
            ),
        )

    @property
    def auto_raise_exceptions(self) -> bool:
        return cast(
            bool,
            self.config.get(
                "auto_raise_exceptions",
                True,
            ),
        )

    @property
    def environment_name(self) -> str:
        return cast(
            str,
            self.config["environment"],
        )
