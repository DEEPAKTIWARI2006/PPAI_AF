# pages/base_page.py
from playwright.sync_api import expect
from utils.logger import get_logger

class BasePage:
    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url
        self.logger = get_logger(self.__class__.__name__)
        
    def open(self, path: str =""):
        url = f"{self.base_url}{path}"
        self.logger.info(f"Launching URL: {url}")
        self.page.goto(url)

    def click(self, locator):
        self.logger.info(f"Clicking on element: {locator}")
        self.page.wait_for_selector(locator, state="visible")
        self.page.click(locator)

    def fill(self, locator, value):
        self.logger.info(f"Entering value: {value} into element: {locator}")
        self.page.wait_for_selector(locator, state="visible")
        self.page.fill(locator, value)

    def get_text(self, locator):
        self.page.wait_for_selector(locator, state="visible")
        return self.page.text_content(locator)

    def is_visible(self, locator):
        return self.page.is_visible(locator)

    def assert_visible(self, locator):
        expect(self.page.locator(locator)).to_be_visible()
