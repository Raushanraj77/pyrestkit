from src.config.config import ConfigManager


def test_load_dev_config() -> None:
    config = ConfigManager("dev")

    assert config.environment_name == "dev"
    assert config.timeout == 30
    assert config.base_url == "https://reqres.in/api"
