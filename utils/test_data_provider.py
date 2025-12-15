from utils.test_data_store import TestDataStore


class TestDataProvider:

    @staticmethod
    def get_data(test_id: str, data_set: str = None) -> list:
        test_data = TestDataStore.get_test_data(test_id)

        if not test_data:
            return []

        if data_set:
            return test_data.get(data_set, [])

        # If no dataset specified → flatten all datasets
        all_data = []
        for records in test_data.values():
            all_data.extend(records)

        return all_data
