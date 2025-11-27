from utils.logger import get_logger
from playwright.sync_api import TimeoutError as PlaywrightTimeout

class BasePage:
    def __init__(self, context):
        self.context = context
        self.page = context.page
        self.logger = get_logger(self.__class__.__name__)

    # --- All common functions ---

    def open(self, url: str):
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url)
        self.page.wait_for_load_state("load")
        

    def click(self, locator: str):
        self.logger.info(f"Clicking: {locator}")
        self.wait_for_visible(locator)
        self.page.click(locator)

    def fill(self, locator: str, value: str):
        self.logger.info(f"Filling: {locator} with value: {value}")
        self.wait_for_visible(locator)
        self.page.fill(locator, value)
        self.page

    def get_text(self, locator: str) -> str:
        self.wait_for_visible(locator)
        text = self.page.inner_text(locator)
        self.logger.info(f"Text of {locator}: {text}")
        return text

    def wait_for_visible(self, locator: str, timeout: float = 5000):
        try:
            self.logger.info(f"Waiting for element visible: {locator}")
            self.page.wait_for_selector(locator, timeout=timeout, state="visible")
        except PlaywrightTimeout:
            self.logger.error(f"Timeout waiting for: {locator}")
            raise
