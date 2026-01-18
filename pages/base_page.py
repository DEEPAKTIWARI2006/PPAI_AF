# pages/base_page.py
import allure
from playwright.sync_api import expect


class BasePage:
    def __init__(self, page, base_url, logger):
        if logger is None:
            raise ValueError("Logger must be provided to BasePage")
        self.page = page
        self.base_url = base_url
        self.logger = logger

    def _resolve_locator(self, locator, **dynamic_values):
        locator_type = locator[0]

        if locator_type in ("css", "xpath"):
            selector = self._format_dynamic_values(locator[1], **dynamic_values)
            return self.page.locator(selector)

        if locator_type == "text":
            text = self._format_dynamic_values(locator[1], **dynamic_values)
            return self.page.get_by_text(text)

        if locator_type == "role":
            role = locator[1]
            params = locator[2] if len(locator) > 2 else {}
            formatted_params = self._format_dynamic_values(params, **dynamic_values)
            return self.page.get_by_role(role, **formatted_params)

        if locator_type == "label":
            label = self._format_dynamic_values(locator[1], **dynamic_values)
            return self.page.get_by_label(label)

        raise ValueError(f"Unsupported locator type: {locator_type}")

    def _format_dynamic_values(self, obj, **dynamic_values):
        """
        Recursively formats strings inside dicts/lists using dynamic_values.
        """
        if isinstance(obj, str):
            return obj.format(**dynamic_values)

        if isinstance(obj, dict):
            return {
                key: self._format_dynamic_values(value, **dynamic_values)
                for key, value in obj.items()
            }

        if isinstance(obj, (list, tuple)):
            return [self._format_dynamic_values(item, **dynamic_values) for item in obj]

        return obj

    def open(self, path: str = ""):
        url = f"{self.base_url}{path}"
        self.logger.info(f"Launching URL: {url}")
        self.page.goto(url)

    def click(self, locator, **dynamic_values):
        self.logger.info("Clicking on element")
        element = self._resolve_locator(locator, **dynamic_values)
        element.wait_for(state="visible")
        element.click()

    def fill(self, locator, value, **dynamic_values):
        self.logger.info(f"Filling value [{value}] into field")
        element = self._resolve_locator(locator, **dynamic_values)
        element.wait_for(state="visible")
        element.fill(value)

    # For Checkbox and Radio Button
    def check(self, locator, **dynamic_values):
        self.logger.info("Checking checkbox/radio button")
        element = self._resolve_locator(locator, **dynamic_values)
        element.wait_for(state="attached")
        element.check()

    # for Dropdowns
    def select_by_value(self, locator, value, **dynamic_values):
        self.logger.info(f"Selecting dropdown value [{value}]")
        element = self._resolve_locator(locator, **dynamic_values)
        element.select_option(value)

    # Usage: self.press_key("Tab") / self.press_key("Escape")
    def press_key(self, key: str):
        self.logger.info(f"Pressing keyboard key [{key}]")
        self.page.keyboard.press(key)

    def type_and_enter(self, locator, value, **dynamic_values):
        self.logger.info(f"Typing [{value}] and pressing Enter")
        element = self._resolve_locator(locator, **dynamic_values)
        element.fill(value)
        element.press("Enter")

    def click_when_ready(self, locator, **dynamic_values):
        self.logger.info("Clicking element when ready")
        element = self._resolve_locator(locator, **dynamic_values)
        element.wait_for(state="visible")
        element.wait_for(state="enabled")
        element.click()

    def get_text(self, locator, **dynamic_values) -> str:
        return self._resolve_locator(locator, **dynamic_values).inner_text()

    def get_attribute(self, locator, **dynamic_values) -> str:
        return self._resolve_locator(locator, **dynamic_values).get_attribute(
            "validationMessage"
        )

    def is_visible(self, locator, **dynamic_values) -> bool:
        return self._resolve_locator(locator, **dynamic_values).is_visible()

    def assert_visible(self, locator):
        expect(self.page.locator(locator)).to_be_visible()

    def _wait_for(self, locator, state: str, timeout: int = 5000, **dynamic_values):
        """
        Central wait handler for all locator waits
        """
        element = self._resolve_locator(locator, **dynamic_values)

        self.logger.info(
            f"Waiting for element state='{state}' with timeout={timeout}ms"
        )

        element.wait_for(state=state, timeout=timeout)
        return element

    def wait_for_visible(self, locator, timeout: int = 5000, **dynamic_values):
        return self._wait_for(
            locator, state="visible", timeout=timeout, **dynamic_values
        )

    def wait_for_hidden(self, locator, timeout: int = 5000, **dynamic_values):
        return self._wait_for(
            locator, state="hidden", timeout=timeout, **dynamic_values
        )

    def wait_for_attached(self, locator, timeout: int = 5000, **dynamic_values):
        return self._wait_for(
            locator, state="attached", timeout=timeout, **dynamic_values
        )

    def wait_for_enabled(self, locator, timeout: int = 5000, **dynamic_values):
        element = self.wait_for_visible(locator, timeout, **dynamic_values)
        element.wait_for(state="enabled", timeout=timeout)
        return element

    def is_hidden(self, locator, timeout: int = 3000, **dynamic_values) -> bool:
        try:
            self._wait_for(locator, "hidden", timeout, **dynamic_values)
            return True
        except Exception:
            self.logger.info("Element not hidden")
            return False

    def is_enabled(self, locator, **dynamic_values) -> bool:
        try:
            element = self._resolve_locator(locator, **dynamic_values)
            return element.is_enabled()
        except Exception:
            return False

    def get_count(self, locator, **dynamic_values) -> int:
        element = self._resolve_locator(locator, **dynamic_values)
        count = element.count()
        self.logger.info(f"Element count: {count}")
        return count

    def click_when_visible(self, locator, timeout: int = 5000, **dynamic_values):
        element = self.wait_for_visible(locator, timeout, **dynamic_values)
        element.click()

    # base_page.py
    def get_locator(self, locator, **dynamic_values):
        """
        Resolve a framework locator tuple into a Playwright Locator.

        Args:
        locator: Tuple-based locator definition from locators module
        **dynamic_values: Dynamic placeholders for locator formatting

        Returns:
        playwright.sync_api.Locator
        """
        return self._resolve_locator(locator, **dynamic_values)
