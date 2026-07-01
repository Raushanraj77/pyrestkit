import json
from pathlib import Path


class ConfigManager:
    """
    Loads environment configuration from JSON files.
    1)Path(__file__).parent is used to get the directory of the current file (config.py), and then it appends the environment-specific JSON file name to that path.
    It always starts from the location of config.py, making it portable across operating systems.
    2) Why @property?
        Without it:
            config.get_base_url()
        With it:
            config.base_url
            The second option is cleaner and feels like accessing an attribute, while still allowing us to compute or validate values internally if needed.
    3) Why raise FileNotFoundError?
        Imagine someone runs:
            pytest --env=production
        but there's no production.json.
        Instead of mysterious errors later, the framework fails immediately with a clear message.
    """

    def __init__(self, environment: str = "dev"):
        self.environment = environment.lower()

        config_file = Path(__file__).parent / f"{self.environment}.json"

        if not config_file.exists():
            raise FileNotFoundError(
                f"Configuration file '{config_file.name}' not found."
            )

        with open(config_file, "r") as file:
            self.config = json.load(file)

    @property
    def base_url(self) -> str:
        return self.config["base_url"]

    @property
    def timeout(self) -> int:
        return self.config["timeout"]

    @property
    def headers(self) -> dict:
        return self.config["headers"]

    @property
    def environment_name(self) -> str:
        return self.config["environment"]