import json
from pathlib import Path


class JsonLoader:

    @staticmethod
    def load(file_path: str) -> dict:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Test data file not found: {file_path}")

        with path.open(encoding="utf-8") as f:
            return json.load(f)
