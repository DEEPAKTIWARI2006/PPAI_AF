import json
import logging
import logging.config
from pathlib import Path

_LOGGER_CACHE = {}


def setup_base_logging():
    config_path = Path(__file__).parent.parent / "configs" / "logger_config.json"
    with open(config_path, "r") as f:
        config = json.load(f)

    logging.config.dictConfig(config)

def get_test_logger(test_id: str) -> logging.Logger:
    """
    Creates a dedicated logger per test.
    """
    if test_id in _LOGGER_CACHE:
        return _LOGGER_CACHE[test_id]

    logger = logging.getLogger(test_id)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    log_dir = Path("reports/logs/tests")
    log_dir.mkdir(parents=True, exist_ok=True)

    safe_name = test_id.replace("::", "_").replace("/", "_")
    file_handler = logging.FileHandler(log_dir / f"{safe_name}.log")

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    _LOGGER_CACHE[test_id] = logger
    return logger
