# pages/register_page.py
from locators.register_locators import RegisterLocators
from pages.base_page import BasePage

class RegisterPage(BasePage):
    def __init__(self, page, base_url):
        super().__init__(page, base_url)
        self.loc = RegisterLocators

    def launch_app(self, path):
        self.open(path)

    def register_user(self, first_name, last_name):
        self.fill(self.loc.FIRST_NAME, first_name)
        self.fill(self.loc.LAST_NAME, last_name)
        self.click(self.loc.SUBMIT_BUTTON)