import pytest
import os
import allure
import shutil
from core.config_loader import ConfigLoader
from playwright.sync_api import sync_playwright
from pages.register_page import RegisterPage
from core.browser_factory import BrowserFactory
from core.context_factory import ContextFactory
from utils.logger import get_test_logger
from pathlib import Path
from utils.logger import _LOGGER_CACHE
from utils.test_result_collector import TestResults

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
def register_page(page, base_url, test_logger):
    return RegisterPage(page, base_url, test_logger)

@pytest.fixture
def test_logger(request):
    from utils.logger import get_test_logger
    return get_test_logger(request.node.nodeid)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call":
        test_id = item.nodeid.replace("::", "_").replace("/", "_")
        log_file = Path(f"reports/logs/tests/{test_id}.log")

        if log_file.exists():
            allure.attach(
                log_file.read_text(),
                name="Test Log",
                attachment_type=allure.attachment_type.TEXT
            )
            
@pytest.fixture(scope="session", autouse=True)
def allure_environment_file(env):
    """
    Creates environment.properties file for Allure report.
    """
    results_dir = Path("reports/allure-results")
    results_dir.mkdir(parents=True, exist_ok=True)

    env_file = results_dir / "environment.properties"

    browser = os.getenv("BROWSER", "chromium")

    env_file.write_text(
        f"Environment={env}\n"
        f"Browser={browser}\n"
    )
    
def pytest_sessionstart(session):
    """
    Clean reports BEFORE any tests or workers start.
    Safe for pytest-xdist and Windows.
    """

    paths_to_clean = [
        Path("reports/logs"),
        Path("reports/allure-results"),
        Path("reports/allure-report")
    ]

    for path in paths_to_clean:
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)

        path.mkdir(parents=True, exist_ok=True)
        
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call" and result.failed:
        page = item.funcargs.get("page")
        if page:
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )