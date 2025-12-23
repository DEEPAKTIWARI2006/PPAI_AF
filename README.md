This is a Pyhon & Playwright automation framework
# PPAI_AF — Python Playwright Automation Framework

This repository contains a Python-based automation framework using Playwright and pytest. It implements Page Object Model (POM), data-driven testing utilities, and integrates Allure reporting. The framework is designed for UI and API test automation, and it can be executed locally, via Docker, or in CI (Azure Pipelines / GitHub Actions).

---

Table of contents
- Overview
- Architecture & key components
- Prerequisites
- Quick start (local)
- Running tests (examples)
- Running tests in Docker (and CI)
- Reporting (Allure & PDF)
- Configuration & environment variables
- Project structure
- How to add tests
- Markers & test selection
- Troubleshooting & common issues
- Best practices & conventions
- Roadmap / Improvements
- Maintainers / Contact
- License

---

Overview
--------
This framework targets functional UI tests (Playwright) and API tests using pytest. It uses:
- Playwright for browser automation
- pytest as the test runner
- Allure for reporting
- Page Object Model structure (pages/)
- Utilities for data loading and test data providers
- Fixtures and centralized failure handling in `conftest.py` (screenshots & log attachments on failures)

Key goals:
- Modular and extensible
- Data-driven tests
- CI-ready
- Rich reporting with Allure

---

Architecture & key components
-----------------------------
- pages/ - page object classes (UI)
- core/ - BrowserFactory, ContextFactory, ConfigLoader
- utils/ - helpers (json loader, data providers, logger, pdf generator, failure classifier)
- tests/ - grouped tests (ui_tests, api_tests)
- data/ - test data JSON files
- reports/ - allure results and generated HTML reports
- configs/ - environment configs (yaml)
- conftest.py - pytest fixtures and hooks

---

Prerequisites
-------------
- Python 3.11+
- pip
- git
- Playwright (browsers installed via `playwright install`)
- Allure CLI (optional, for generating HTML from allure-results)
- Docker (optional, recommended for CI parity)

---

Quick start (local)
-------------------
1. Clone:
   git clone https://github.com/DEEPAKTIWARI2006/PPAI_AF.git
   cd PPAI_AF

2. Virtual env:
   python -m venv .venv
   source .venv/bin/activate   # macOS / Linux
   .venv\Scripts\activate      # Windows

3. Install dependencies:
   pip install --upgrade pip
   pip install -r requirements.txt

4. Install Playwright browsers:
   playwright install chromium

5. Provide environment variables (or copy `.env.txt` to `.env`):
   TEST_ENV=qa
   BROWSER=chromium
   TEST_DATA_FILE=data/register.json

6. Run tests:
   pytest -v --alluredir=reports/allure-results

---

Running tests (examples)
------------------------
- All tests:
  pytest -v --alluredir=reports/allure-results

- Smoke tests:
  pytest -m smoke --alluredir=reports/allure-results

- Parallel:
  pytest -n 4 --alluredir=reports/allure-results

---

Running in Docker (example)
---------------------------
# using the repository Dockerfile
docker build -t ppaf-tests .
docker run --rm -e TEST_ENV=qa -e BROWSER=chromium -v "$(pwd)":/app ppaf-tests

CI (Azure Pipelines or GitHub Actions) should run tests with the same Docker image or the official Playwright image.

---

Reporting
---------
- Allure results directory: reports/allure-results (set in pytest.ini)
- Generate HTML locally:
  allure generate reports/allure-results -o reports/allure-report --clean
  allure open reports/allure-report

- On failure: screenshots, logs and context are attached to Allure by conftest.py.

---

Configuration & env vars
------------------------
- TEST_ENV — environment name (qa, staging, prod)
- BROWSER — chromium | firefox | webkit
- TEST_DATA_FILE — path to test data JSON
- USERNAME / PASSWORD — credentials for tests

Configs are loaded from configs/{env}.yaml by ConfigLoader.

---

Project structure
-----------------
- core/
- pages/
- utils/
- tests/
- data/
- configs/
- reports/
- conftest.py
- pytest.ini
- requirements.txt
- azure-pipelines.yml
- .github/workflows/ci.yml

---

How to add tests
----------------
- Use page objects from pages/
- Keep tests small and focused
- Use TestDataProvider for data-driven tests
- Use markers for grouping

Markers declared:
- smoke, regression, negative, api, test_id

---

Troubleshooting (quick)
-----------------------
- TypeError: ConfigLoader.get_base_url() takes 1 positional argument but 2 were given
  -> Update ConfigLoader to accept env (provided in this branch) or call it without args.

- Unknown mark warning:
  -> Ensure pytest.ini is present at project root.

- Playwright browsers missing:
  -> Run `playwright install chromium`

---

Roadmap
-------
- Add GitHub Actions (included)
- Add more environment configs
- Add CONTRIBUTING, CODEOWNERS, CHANGELOG

---

Maintainers
-----------
- Repo owner: DEEPAKTIWARI2006

---

License
-------
Add a LICENSE file; MIT recommended.
