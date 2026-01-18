from locators.login_locators import LoginLocators
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page, base_url, logger):
        super().__init__(page, base_url, logger)
        self.loc = LoginLocators

    def launch_app(self, path):
        self.logger.info("Launching Login Page")
        self.open(path)
        # self.click(self.loc.SIGNIN_BUTTON)

    def login_user(self, data):
        self.fill(self.loc.USERNAME, data.username)
        self.fill(self.loc.PASSWORD, data.password)
        self.wait_for_visible(self.loc.LOGIN_BUTTON)
        self.click(self.loc.LOGIN_BUTTON)
        # self.logger.info("Error message captured is" + self.get_attribute(self.loc.FIRST_NAME))
        
        if data.expected == "error":
            self.logger.info("Registration is expected to throw error")
        # if self.is_visible(self.loc.ERROR_MESSAGE_BY_TEXT, error_text="Email is required"):
        #     self.logger.info("Validation error shown")

    # ──────────────────────────────
    # Validations
    # ──────────────────────────────
    def is_error_message_displayed(self, error_text: str) -> bool:
        self.logger.info(f"Checking error message visibility: {error_text}")
        return self.is_visible(self.loc.ERROR_MESSAGE_BY_TEXT, error_text=error_text)