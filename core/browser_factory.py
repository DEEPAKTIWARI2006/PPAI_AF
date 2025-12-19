import os
from playwright.sync_api import Playwright
from core.browser_config import BrowserConfig


class BrowserFactory:

    @staticmethod
    def launch_browser(playwright: Playwright):

        # Load browser configuration from BrowserConfig class
        config = BrowserConfig.load()

        # -----------------------------
        # 1. Read defaults
        # -----------------------------
        defaults = config["defaults"]

        # -----------------------------
        # 2. Determine browser name
        # -----------------------------
        browser_name = os.getenv("BROWSER", "chromium")
        if browser_name not in config["browsers"]:
            raise ValueError(f"Browser '{browser_name}' not found in browser_config.json")

        browser_cfg = config["browsers"][browser_name]

        # -----------------------------
        # 3. Resolve headless mode
        # Priority: ENV > browser > defaults
        # -----------------------------
        if "HEADLESS" in os.environ:
            headless = os.getenv("HEADLESS").lower() == "true"
        else:
            headless = browser_cfg.get("headless", defaults["headless"])

        # -----------------------------
        # 4. Resolve slow_mo
        # -----------------------------
        slow_mo = int(os.getenv("SLOW_MO", defaults.get("slow_mo", 0)))

        # -----------------------------
        # 5. Build launch options
        # -----------------------------
        launch_options = {
            "headless": headless,
            "slow_mo": slow_mo
        }

        if "channel" in browser_cfg:
            launch_options["channel"] = browser_cfg["channel"]

        # -----------------------------
        # 6. Launch browser
        # -----------------------------
        engine_name = browser_cfg["engine"]
        browser_engine = getattr(playwright, engine_name)

        browser = browser_engine.launch(**launch_options)
        return browser
