import json
import os
from pathlib import Path
from utils.logger import get_test_logger


class ConfigLoader:
    _config = None
    _logger = get_test_logger("ConfigLoader")

    @classmethod
    def load_config(cls):
        if cls._config is None:
            env = os.getenv("TEST_ENV", "qa")
            config_path = (
                Path(__file__).parent.parent / "configs" / "env_config.json"
            )

            if not config_path.exists():
                raise FileNotFoundError(f"Config file not found: {config_path}")

            with config_path.open() as f:
                all_config = json.load(f)

            if env not in all_config:
                raise ValueError(f"Environment '{env}' not found in config")

            cls._config = all_config[env]
            cls._logger.info(f"Loaded config for environment: {env}")

        return cls._config

    @classmethod
    def get_base_url(cls) -> str:
        config = cls.load_config()
        base_url = config.get("base_url")

        if not base_url:
            raise KeyError("Missing 'base_url' in environment config")

        cls._logger.info(f"Base URL: {base_url}")
        return base_url

    @classmethod
    def get_api_base_url(cls) -> str:
        config = cls.load_config()
        api_base_url = config.get("api_base_url")

        if not api_base_url:
            raise KeyError("Missing 'api_base_url' in environment config")

        cls._logger.info(f"API Base URL: {api_base_url}")
        return api_base_url
