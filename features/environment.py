from playwright.sync_api import sync_playwright
from pages.page_factory import PageFactory
import allure
import os
import time

def before_all(context):
    print(">>> before_all executed")
    context.playwright = sync_playwright().start()

def before_scenario(context, scenario):
    print(">>> before_scenario executed")
    # New browser context per scenario = clean browser = no leakage
    context.browser = context.playwright.chromium.launch(headless=False)
    context.browser_context = context.browser.new_context()
    context.page = context.browser_context.new_page()

    # Attach PageFactory
    context.factory = PageFactory

def after_scenario(context, scenario):
    print(">>> after_scenario executed")
    if scenario.status == "failed":
        screenshot_path = f"screenshots/{scenario.name}_{int(time.time())}.png"
        context.page.screenshot(path=screenshot_path)
        allure.attach.file(
            screenshot_path,
            name="Failure Screenshot",
            attachment_type=allure.attachment_type.PNG
        )
    context.page.close()
    context.browser_context.close()
    context.browser.close()

def after_all(context):
    print(">>> after_all executed")
    context.playwright.stop()
