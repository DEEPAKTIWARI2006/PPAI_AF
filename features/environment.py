import json
import os
import time
import allure
from playwright.sync_api import sync_playwright
from pages.page_factory import PageFactory


# -------------------- CONFIG LOADER --------------------
def load_config():
    config_path = os.path.join(os.getcwd(), "configs", "browser_config.json")
    print(f"Loading config from: {config_path}")
    with open(config_path, "r") as f:
        return json.load(f)


# -------------------- HOOKS --------------------
def before_all(context):
    print(">>> before_all executed")
    context.config = load_config()
    context.playwright = sync_playwright().start()


def before_scenario(context, scenario):
    print(">>> before_scenario executed")

    cfg = context.config

    platform = cfg.get("platform", "desktop").lower()
    browser_name = cfg.get("browser", "chromium").lower()
    headless = cfg.get("headless", True)
    slow_mo = cfg.get("slow_mo", 0)

    viewport = cfg.get("viewport", {"width": 1920, "height": 1080})
    video = cfg.get("video", "on")
    trace = cfg.get("trace", "on")

    # Safe device config load
    mobile_emulation = cfg.get("devices", {}).get("mobile_emulation", {})
    android_cfg = cfg.get("android", {})

    # ---------------- DESKTOP WEB EXECUTION ----------------
    if platform == "desktop":

        # Select browser
        if browser_name in ["chromium", "chrome"]:
            launch_browser = context.playwright.chromium
        elif browser_name == "firefox":
            launch_browser = context.playwright.firefox
        elif browser_name == "webkit":
            launch_browser = context.playwright.webkit
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        video_dir = f"videos/{scenario.name.replace(' ', '_')}"
        os.makedirs(video_dir, exist_ok=True)

        context.browser = launch_browser.launch(
            headless=headless,
            slow_mo=slow_mo
        )

        # ---- Mobile Emulation ----
        if mobile_emulation.get("enabled", False):
            device_name = mobile_emulation.get("device_name")
            device_profile = context.playwright.devices.get(device_name)

            if not device_profile:
                raise ValueError(f"Playwright device '{device_name}' not found.")

            context.browser_context = context.browser.new_context(
                **device_profile,
                record_video_dir=video_dir if video == "on" else None
            )

        # ---- Desktop Browser ----
        else:
            context.browser_context = context.browser.new_context(
                viewport=viewport,
                record_video_dir=video_dir if video == "on" else None
            )

        if trace == "on":
            context.browser_context.tracing.start(screenshots=True, snapshots=True)

        context.page = context.browser_context.new_page()

    # ---------------- ANDROID DEVICE EXECUTION ----------------
    elif platform == "android":
        print(">>> Launching tests on Android device")

        if not android_cfg.get("enabled", False):
            raise RuntimeError("Android platform selected but 'android.enabled' is false.")

        device_serial = android_cfg.get("device_serial", None)
        package = android_cfg.get("package", "com.android.chrome")
        context.device = context.playwright.android.connect_over_adb(serial=device_serial)
        context.browser_context = context.device.launch_browser(package_name=package)
        context.page = context.browser_context.new_page()
        context.browser = None

    else:
        raise ValueError(f"Unknown platform: {platform}")

    # Attach POM factory
    context.factory = PageFactory


# ---------------- AFTER SCENARIO ----------------
def after_scenario(context, scenario):
    print(">>> after_scenario executed")

    cfg = context.config
    platform = cfg.get("platform", "desktop")
    screenshot_behavior = cfg.get("screenshot", "only-on-failure")

    # Screenshot on failure
    if scenario.status == "failed" and screenshot_behavior in ["on", "only-on-failure"]:
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = f"screenshots/{scenario.name}_{int(time.time())}.png"
        context.page.screenshot(path=screenshot_path)

        allure.attach.file(
            screenshot_path,
            name="Failure Screenshot",
            attachment_type=allure.attachment_type.PNG
        )

    # ---- Trace ----
    try:
        if platform == "desktop" and cfg.get("trace") == "on":
            trace_dir = f"traces/{scenario.name.replace(' ', '_')}"
            os.makedirs(trace_dir, exist_ok=True)
            context.browser_context.tracing.stop(path=f"{trace_dir}/trace.zip")
    except Exception as e:
        print(f"Trace stop error: {e}")

    # ---- Desktop shutdown ----
    if platform == "desktop":
        try:
            context.page.close()
            context.browser_context.close()
            context.browser.close()
        except:
            pass

    # ---- Android shutdown ----
    elif platform == "android":
        try:
            context.browser_context.close()
            context.device.close()
        except Exception as e:
            print(f"Android close error: {e}")


def after_all(context):
    print(">>> after_all executed")
    context.playwright.stop()
