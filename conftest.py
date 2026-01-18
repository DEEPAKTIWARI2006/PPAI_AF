import os
import shutil
from pathlib import Path
import pytest
import allure
from playwright.sync_api import sync_playwright
from collections import defaultdict
from pages.login_page import LoginPage
from utils.failure_classifier import classify_failure
from core.config_loader import ConfigLoader
from core.browser_factory import BrowserFactory
from core.context_factory import ContextFactory
from pages.register_page import RegisterPage
from utils.logger import get_test_logger
from utils.pdf_report_generator import generate_pdf_report
from _pytest.reports import TestReport
from utils.test_data_loader import TestDataLoader
from data_models.data_factory import DataFactory

# Only business markers should appear in reports
ALLOWED_MARKERS = {"api", "smoke", "regression"}


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

    for path in paths_to_clean:
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)
        path.mkdir(parents=True, exist_ok=True)

    env = os.getenv("TEST_ENV", "qa")
    browser = os.getenv("BROWSER", "chromium")

    env_file = Path("reports/allure-results/environment.properties")
    env_file.write_text(f"Environment={env}\n" f"Browser={browser}\n")


# ---------------------------------------------------------
# Environment & config fixtures
# ---------------------------------------------------------
@pytest.fixture(scope="session")
def env():
    return os.getenv("TEST_ENV", "qa")


@pytest.fixture(scope="session")
def base_url(env):
    return ConfigLoader.get_base_url()


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright


# ---------------------------------------------------------
# Playwright page fixture (function-scoped, safe default)
# ---------------------------------------------------------
@pytest.fixture(scope="function")
def page(playwright_instance):
    browser = BrowserFactory.launch_browser(playwright_instance)
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
def login_page(page, base_url, test_logger):
    return LoginPage(page, base_url, test_logger)


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

    if result.when == "call":
        # Store ONLY business markers on the report
        result.business_markers = [
            m.name
            for m in item.iter_markers()
            if m.name in {"api", "smoke", "regression"}
        ]

    if result.failed:
        # Screenshot
        page = item.funcargs.get("page")
        if page:
            try:
                screenshot = page.screenshot()
                allure.attach(
                    screenshot,
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG,
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
                attachment_type=allure.attachment_type.TEXT,
            )


# ---------------------------------------------------------
# Final aggregated summary + PDF generation (retry-safe)
# ---------------------------------------------------------


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    Enterprise-safe pytest summary aggregation.

    ✔ No pytest internal noise
    ✔ Only business markers
    ✔ Retry-safe
    ✔ Warning-safe
    ✔ Zero-test safe
    """

    # --------------------------------------------------
    # Guard: no tests collected
    # --------------------------------------------------
    if terminalreporter._numcollected == 0:
        print("[WARN] No tests collected. Skipping PDF generation.")
        return

    final_reports = {}

    # --------------------------------------------------
    # Collect ONLY final call-phase TestReports
    # --------------------------------------------------
    for reports in terminalreporter.stats.values():
        for report in reports:

            if not isinstance(report, TestReport):
                continue

            if report.when != "call":
                continue

            # Retry-safe: last attempt wins
            final_reports[report.nodeid] = report

    # --------------------------------------------------
    # Aggregate results
    # --------------------------------------------------
    total = len(final_reports)
    passed = failed = skipped = 0
    marker_summary = {}

    for report in final_reports.values():

        # Overall outcome
        if report.outcome == "passed":
            passed += 1
        elif report.outcome == "failed":
            failed += 1
        elif report.outcome == "skipped":
            skipped += 1

        # --------------------------------------------------
        # Use markers captured earlier
        # --------------------------------------------------
        markers = getattr(report, "business_markers", [])

        if not markers:
            continue

        for marker in markers:
            marker_summary.setdefault(
                marker,
                {"passed": 0, "failed": 0, "skipped": 0, "duration": 0, "failures": {}},
            )

            marker_summary[marker][report.outcome] += 1
            marker_summary[marker]["duration"] += getattr(report, "duration", 0)

    # --------------------------------------------------
    # Build summary
    # --------------------------------------------------
    summary = {
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "markers": marker_summary,
    }

    # --------------------------------------------------
    # Generate PDF
    # --------------------------------------------------
    from utils.pdf_report_generator import generate_pdf_report

    generate_pdf_report(summary)


@pytest.fixture
def test_data(request):
    flow = request.node.get_closest_marker("flow").args[0]
    test_case_id = request.node.get_closest_marker("test_id").args[0]
    category = request.node.get_closest_marker("category").args[0]

    raw = TestDataLoader.load(flow=flow, test_case_id=test_case_id, category=category)

    return DataFactory.create(
        flow=flow, raw=raw, test_case_id=test_case_id, category=category
    )
