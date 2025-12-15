import pytest
from pages.register_page import RegisterPage

@pytest.mark.regression
@pytest.mark.test_id("TC01")
def test_register_data1(register_page, test_data):

    register_page.launch_app("/Register.html")
    register_page.register_user(test_data["firstname"], test_data["lastname"])

@pytest.mark.regression
@pytest.mark.test_id("TC02")
def test_register_data2(register_page, test_data):

    register_page.launch_app("/Register.html")
    register_page.register_user(test_data["firstname"], test_data["lastname"])
