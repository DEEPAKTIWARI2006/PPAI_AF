# pages/register_page.py
from locators.register_locators import RegisterLocators
from pages.base_page import BasePage


class RegisterPage(BasePage):
    def __init__(self, page, base_url, logger):
        super().__init__(page, base_url, logger)
        self.loc = RegisterLocators

    def launch_app(self, path):
        self.logger.info("Launching Registration Page")
        self.open(path)

    def register_user(self, data):
        self.fill(self.loc.FIRST_NAME, data.firstname)
        self.fill(self.loc.LAST_NAME, data.lastname)
        self.fill(self.loc.ADDRESS, data.address)
        self.fill(self.loc.EMAIL, data.email)
        self.fill(self.loc.PHONE, data.phone)
        self.check(self.loc.GENDER, gender=data.gender)
        for hobby in data.hobbies:
            self.check(self.loc.HOBBY, hobby=hobby)
        self.click(self.loc.LANGUAGE_DROPDOWN)
        for language in data.languages:
            self.click(self.loc.LANGUAGE_OPTION_BY_TEXT, language=language)
        self.click(self.loc.FORM_BODY)
        self.click(self.loc.SKILLS_SELECT)
        self.select_by_value(self.loc.SKILLS_SELECT, data.skills)
        self.click(self.loc.COUNTRY_SEARCH)
        self.click(self.loc.COUNTRY_OPTION_BY_NAME, country=data.country)
        self.select_by_value(self.loc.DOB_YEAR_SELECT, data.dob_year)
        self.select_by_value(self.loc.DOB_MONTH_SELECT, data.dob_month)
        self.select_by_value(self.loc.DOB_DAY_SELECT, data.dob_day)
        self.fill(self.loc.PASSWORD, data.password)
        self.fill(self.loc.CONFIRM_PASSWORD, data.confirm_password)

        self.wait_for_visible(self.loc.SUBMIT_BUTTON)
        self.click(self.loc.SUBMIT_BUTTON)

    # ──────────────────────────────
    # Validations
    # ──────────────────────────────
    def is_error_message_displayed(self, data) -> bool:
        country_drop_down = self.get_locator(self.loc.COUNTRY_WITH_ERROR)
        error_text_actual = country_drop_down.evaluate(
            """
                                (el) => ({
                                 valid: el.checkValidity(),
                                 message: el.validationMessage
                                })
                                """
        )
        self.logger.info(f"Actual displayed error: {error_text_actual}")
        self.logger.info(f"Expected displayed error: {data.expected_err}")

        if data.expected_err == error_text_actual["message"]:
            self.logger.info("Error message matched as expected")
            return True
        else:
            self.logger.info("error message did not match")
            return False

    def select_language(self, language: str):
        self.logger.info(f"Selecting language: {language}")
        self.click(self.loc.LANGUAGE_DROPDOWN)
        self.click(self.loc.LANGUAGE_OPTION_BY_TEXT, language=language)

    def select_skill(self, skill: str):
        self.logger.info(f"Selecting skill: {skill}")
        self.select_by_value(self.loc.SKILLS_SELECT, skill)

    def submit_form(self):
        self.logger.info("Submitting registration form")
        self.click(self.loc.SUBMIT_BUTTON)

    def submit_if_enabled(self):
        if self.is_enabled(self.loc.SUBMIT_BUTTON):
            self.click(self.loc.SUBMIT_BUTTON)
