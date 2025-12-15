import time
import pytest
from pages.register_page import RegisterPage

@pytest.mark.test_id("TC01")
@pytest.mark.smoke
def test_register_data1(register_page, test_data):

    register_page.launch_app("/Register.html")
    register_page.register_user(test_data["firstname"], test_data["lastname"])

@pytest.mark.test_id("TC02")
@pytest.mark.smoke
def test_register_data2(register_page, test_data):

    register_page.launch_app("/Register.html")
    register_page.register_user(test_data["firstname"], test_data["lastname"])
    