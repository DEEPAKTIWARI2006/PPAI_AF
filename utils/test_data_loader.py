import json
from pathlib import Path


class TestDataLoader:
    """
    Generic loader for all flow-based JSON files
    """

    BASE_PATH = Path("test_data")

    @classmethod
    def load(cls, flow: str, test_case_id: str, category: str) -> dict:
        file_path = cls.BASE_PATH / f"{flow}_data.json"

        if not file_path.exists():
            raise FileNotFoundError(f"Test data file not found: {file_path}")

        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        if test_case_id not in data:
            raise KeyError(f"{test_case_id} not found in {file_path.name}")

        if category not in data[test_case_id]:
            raise KeyError(
                f"Category '{category}' not found under {test_case_id}"
            )

        # Return FIRST record (extend later if you want iteration)
        return data[test_case_id][category][0]
