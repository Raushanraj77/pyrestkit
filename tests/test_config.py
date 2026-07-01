from src.config.config import ConfigManager


def test_load_dev_config():
    config = ConfigManager("dev")

    assert config.environment_name == "DEV"
    assert config.timeout == 30
    assert config.base_url == "https://reqres.in/api"