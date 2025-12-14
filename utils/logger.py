import json
import logging
import logging.config
from pathlib import Path

_CONFIGURED = False


def setup_logging():
    """
    Configure logging once per test session.
    """
    global _CONFIGURED
    if _CONFIGURED:
        return

    config_path = Path(__file__).parent.parent / "configs" / "logger_config.json"

    with open(config_path, "r") as f:
        config = json.load(f)

    # Ensure log directory exists
    log_file = Path(config["handlers"]["file"]["filename"])
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logging.config.dictConfig(config)
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    setup_logging()
    return logging.getLogger(name)
