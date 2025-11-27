from playwright.sync_api import Page

def take_screenshot(page: Page, path: str):
    page.screenshot(path=path, full_page=True)
