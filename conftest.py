import os
import shutil
from pathlib import Path
from utils.data_loaders.json_loader import JsonLoader
from utils.test_data_store import TestDataStore
from utils.test_data_provider import TestDataProvider
import pytest
import allure
from playwright.sync_api import sync_playwright
from collections import defaultdict
from utils.failure_classifier import classify_failure
from core.config_loader import ConfigLoader
from core.browser_factory import BrowserFactory
from core.context_factory import ContextFactory
from pages.register_page import RegisterPage
from utils.logger import get_test_logger
from utils.pdf_report_generator import generate_pdf_report
from utils.test_data_provider import TestDataProvider


# ---------------------------------------------------------
# Session start: clean reports + create Allure env metadata
# ---------------------------------------------------------
def pytest_sessionstart(session):
    """
    Runs once in MASTER process before workers start.
    Cleans reports and creates Allure environment file.
    """

    paths_to_clean = [
        Path("reports/logs"),
        Path("reports/allure-results"),
        Path("reports/allure-report"),
    ]
    
    data_file = os.getenv("TEST_DATA_FILE", "data/register.json")
    json_data = JsonLoader.load(data_file)
    TestDataStore.initialize(json_data)

    for path in paths_to_clean:
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)
        path.mkdir(parents=True, exist_ok=True)

    env = os.getenv("TEST_ENV", "qa")
    browser = os.getenv("BROWSER", "chromium")

    env_file = Path("reports/allure-results/environment.properties")
    env_file.write_text(
        f"Environment={env}\n"
        f"Browser={browser}\n"
    )


# ---------------------------------------------------------
# Environment & config fixtures
# ---------------------------------------------------------
@pytest.fixture(scope="session")
def env():
    return os.getenv("TEST_ENV", "qa")


@pytest.fixture(scope="session")
def base_url(env):
    return ConfigLoader.get_base_url(env)


# ---------------------------------------------------------
# Playwright page fixture (function-scoped, safe default)
# ---------------------------------------------------------
@pytest.fixture(scope="function")
def page():
    with sync_playwright() as playwright:
        browser = BrowserFactory.launch_browser(playwright)
        context = ContextFactory.create_context(browser)
        page = context.new_page()
        yield page
        context.close()
        browser.close()


# ---------------------------------------------------------
# Logger fixture (per test)
# ---------------------------------------------------------
@pytest.fixture
def test_logger(request):
    return get_test_logger(request.node.nodeid)


# ---------------------------------------------------------
# Page object fixture
# ---------------------------------------------------------
@pytest.fixture
def register_page(page, base_url, test_logger):
    return RegisterPage(page, base_url, test_logger)


# ---------------------------------------------------------
# Central hook: screenshots + logs on FAILURE only
# ---------------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Central failure handling:
    - Screenshot on failure
    - Attach per-test log to Allure
    """

    outcome = yield
    result = outcome.get_result()

    if result.when != "call":
        return

    if result.failed:
        # Screenshot
        page = item.funcargs.get("page")
        if page:
            try:
                screenshot = page.screenshot()
                allure.attach(
                    screenshot,
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"[WARN] Screenshot capture failed: {e}")

        # Attach test log
        test_id = item.nodeid.replace("::", "_").replace("/", "_")
        log_file = Path(f"reports/logs/tests/{test_id}.log")

        if log_file.exists():
            allure.attach(
                log_file.read_text(),
                name="Test Log",
                attachment_type=allure.attachment_type.TEXT
            )


# ---------------------------------------------------------
# Final aggregated summary + PDF generation (retry-safe)
# ---------------------------------------------------------

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    final_reports = {}

    for _, reports in terminalreporter.stats.items():
        for report in reports:
            if report.when != "call":
                continue
            final_reports[report.nodeid] = report

    declared_markers = {
        m.split(":")[0].strip()
        for m in config.getini("markers")
    }

    summary = {
        "total": len(final_reports),
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "markers": defaultdict(lambda: {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "duration": 0.0,
            "failures": defaultdict(int)
        })
    }

    for report in final_reports.values():
        outcome = report.outcome
        duration = getattr(report, "duration", 0.0)

        summary[outcome] += 1

        real_markers = [
            m for m in report.keywords if m in declared_markers
        ] or ["unmarked"]

        for marker in real_markers:
            m = summary["markers"][marker]
            m[outcome] += 1
            m["duration"] += duration

            if outcome == "failed":
                failure_type = classify_failure(report.longrepr)
                m["failures"][failure_type] += 1

    generate_pdf_report(summary)

import pytest
from utils.test_data_provider import TestDataProvider





def pytest_generate_tests(metafunc):
    """
    Dynamically parametrize tests that use `test_data`.
    """

    if "test_data" not in metafunc.fixturenames:
        return

    node = metafunc.definition
    test_id_marker = node.get_closest_marker("test_id")

    if not test_id_marker:
        raise ValueError(
            f"{node.name} is missing @pytest.mark.test_id"
        )

    test_id = test_id_marker.args[0]

    # Dataset from marker (smoke / regression / negative)
    dataset_marker = (
        node.get_closest_marker("smoke")
        or node.get_closest_marker("regression")
        or node.get_closest_marker("negative")
    )

    data_set = dataset_marker.name if dataset_marker else None

    data = TestDataProvider.get_data(test_id, data_set)

    if not data:
        raise ValueError(
            f"No test data found for test_id={test_id}, data_set={data_set}"
        )

    # 🔑 Key line: pytest handles iteration
    metafunc.parametrize("test_data", data)
