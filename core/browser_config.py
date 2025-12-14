import json
from pathlib import Path

class BrowserConfig:
    _config = None

    @classmethod
    def load(cls):
        if cls._config is None:
            config_path = Path(__file__).parent.parent / "configs" / "browser_config.json"
            with open(config_path, "r") as f:
                cls._config = json.load(f)
        return cls._config
