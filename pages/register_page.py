# pages/register_page.py
from locators.register_locators import RegisterLocators
from locators.locator_resolver import LocatorResolver
from pages.base_page import BasePage


class RegisterPage(BasePage):
    def __init__(self, page, base_url, logger):
        super().__init__(page, base_url, logger)
        self.loc = RegisterLocators

    def launch_app(self, path):
        self.logger.info("Launching Registration Page")
        self.open(path)

    def register_user(self, first_name, last_name):
        self.logger.info("Entering first name")
        self.fill(self.loc.FIRST_NAME, first_name)
        self.logger.info("Entering last name")
        self.fill(self.loc.LAST_NAME, last_name)
        self.click(self.loc.SUBMIT_BUTTON)
        
def is_error_message_displayed(self, error_text: str) -> bool:
        locator = LocatorResolver.resolve(
            RegisterLocators.ERROR_MESSAGE_BY_TEXT,
            error_text=error_text
        )
        return self.is_visible(locator)