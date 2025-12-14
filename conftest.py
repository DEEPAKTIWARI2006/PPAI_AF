import pytest
import os
from core.config_loader import ConfigLoader
from playwright.sync_api import sync_playwright
from pages.register_page import RegisterPage
from core.browser_factory import BrowserFactory
from core.context_factory import ContextFactory

@pytest.fixture(scope="session")
def env():
    return os.getenv("TEST_ENV", "qa")

@pytest.fixture(scope="session")
def base_url(env):
    return ConfigLoader.get_base_url(env)

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as playwright:
        browser = BrowserFactory.launch_browser(playwright)
        context = ContextFactory.create_context(browser)
        page = context.new_page()
        yield page
        context.close()
        browser.close()
        
@pytest.fixture
def register_page(page, base_url):
    return RegisterPage(page, base_url)