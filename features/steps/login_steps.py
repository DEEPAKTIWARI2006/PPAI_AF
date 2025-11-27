from behave import *
import time

@given('we have behave installed')
def step_impl(context):
    print("Context attributes:", dir(context))
    login = context.factory.get_page(context, "LoginPage")
    login.open_login()

@when('we implement a test')
def step_impl(context):
    login = context.factory.get_page(context, "LoginPage")
    login.enter_username("sdafsdf")
    login.enter_password("wiuertiwer")
    time.sleep(5)  # Small wait to ensure page is fully loaded

@then('behave will test it for us!')
def step_impl(context):
    login = context.factory.get_page(context, "LoginPage")
    # login.click_login()
    # login.verify_dashboard()