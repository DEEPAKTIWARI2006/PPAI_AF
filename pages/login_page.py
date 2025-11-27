from pages.base_page import BasePage
from locators.login_locators import LoginLocators

class LoginPage(BasePage):

    def open_login(self):
        self.logger.info("Opening Login Page")
        self.open("https://demo.automationtesting.in/Register.html")

    def enter_username(self, username):
        self.logger.info(f"Entering first name: {username}")
        self.fill(LoginLocators.FIRST_NAME, username)

    def enter_password(self, password):
        self.logger.info(f"Entering last name: {password}")
        self.fill(LoginLocators.LAST_NAME, password)

    def click_login(self):
        self.logger.info("Clicking login button")
        self.click(LoginLocators.SUBMIT_BUTTON)

    def verify_dashboard(self):
        self.logger.info("Verifying Dashboard page")
        # self.wait_for_visible(LoginLocators.DASHBOARD_HEADER)
