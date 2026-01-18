class LoginData:
    def __init__(self, raw: dict, test_case_id: str, category: str):
        self.username = raw.get("username")
        self.password = raw.get("password")
        self.expected = raw.get("expected")

        # metadata (useful later for reporting/logging)
        self.test_case_id = test_case_id
        self.category = category

    def is_success(self) -> bool:
        return self.expected == "success"

    def is_error(self) -> bool:
        return self.expected == "error"
