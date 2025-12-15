class TestDataStore:
    _data = None

    @classmethod
    def initialize(cls, data: dict):
        if cls._data is None:
            cls._data = data

    @classmethod
    def get_test_data(cls, test_id: str) -> dict:
        if cls._data is None:
            raise RuntimeError("TestDataStore not initialized")
        return cls._data.get(test_id, {})
