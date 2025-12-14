from core.browser_config import BrowserConfig

class ContextFactory:

    @staticmethod
    def create_context(browser):
        config = BrowserConfig.load()

        context_options = {
            "viewport": config.get("viewport"),
            "record_video_dir": "reports/videos" if config.get("video") == "on" else None
        }

        return browser.new_context(**context_options)
