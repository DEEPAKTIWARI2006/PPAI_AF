class RegistrationData:
    def __init__(self, raw: dict, test_case_id: str, category: str):
        self.firstname = raw.get("firstname")
        self.lastname = raw.get("lastname")
        self.address = raw.get("address")
        self.gender = raw.get("gender")
        self.phone = raw.get("phone")
        self.hobbies = raw.get("hobbies")
        self.email = raw.get("email")
        self.languages = raw.get("languages")
        self.skills = raw.get("skills")
        self.country = raw.get("country")
        self.dob_year = raw.get("dob_year")
        self.dob_month = raw.get("dob_month")
        self.dob_day = raw.get("dob_day")
        self.password = raw.get("password")
        self.confirm_password = raw.get("confirm_password")
        self.expected_err = raw.get("expected_err")

        # metadata (useful later for reporting/logging)
        self.test_case_id = test_case_id
        self.category = category

    def is_success(self) -> bool:
        return self.expected == "success"

    def is_error(self) -> bool:
        return self.expected == "error"
