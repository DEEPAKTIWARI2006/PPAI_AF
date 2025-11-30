from playwright.sync_api import sync_playwright 
p = sync_playwright().start() 
pandroid = p.android.connect(device_serial="emulator-5554")
b_android = pandroid.launch_browser(package_name="com.android.chrome")
page_android = b_android.new_page()
page_android.goto("https://example.com") 
print("Page title on Android:", page_android.title())   
p.stop()