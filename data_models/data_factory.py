from data_models.registration_data import RegistrationData
from data_models.login_data import LoginData
class DataFactory:

    @staticmethod
    def create(flow: str, raw: dict, test_case_id: str, category: str):
        if flow == "registration":
            return RegistrationData(raw, test_case_id, category)
        elif flow == "login":
            return LoginData(raw, test_case_id, category)

        raise ValueError(f"No data object defined for flow: {flow}")
