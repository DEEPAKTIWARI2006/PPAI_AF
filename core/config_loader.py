import json
import os
from pathlib import Path

class ConfigLoader:
    _config = None

    @classmethod
    def load_config(cls):
        if cls._config is None:
            config_path = Path(__file__).parent.parent / "configs" / "env_config.json"
            with open(config_path, "r") as f:
                cls._config = json.load(f)
        return cls._config

    @classmethod
    def get_base_url(cls, env: str) -> str:
        config = cls.load_config()
        if env not in config:
            raise ValueError(f"Environment '{env}' not found in config")
        return config[env]["base_url"]
