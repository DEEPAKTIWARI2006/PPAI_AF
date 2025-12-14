import pytest
from pages.register_page import RegisterPage

@pytest.mark.regression
def test_register_data1(register_page):

    register_page.launch_app("/Register.html")
    register_page.register_user("Vivaan", "Tiwari")
    assert register_page.is_error_message_displayed("Invalid username or password")

@pytest.mark.regression
def test_register_data2(register_page, test_logger):

    register_page.launch_app("/Register.html")
    register_page.register_user("Sunil", "Kumar")
    
    
@pytest.mark.regression
def test_register_data5(register_page, test_logger):

    register_page.launch_app("/Register.html")
    register_page.register_user("Alex", "Cruz")
    
@pytest.mark.regression
def test_register_data6(register_page, test_logger):

    register_page.launch_app("/Register.html")
    register_page.register_user("Ajay", "Sharma")
    
@pytest.mark.regression
def test_register_data7(register_page, test_logger):

    register_page.launch_app("/Register.html")
    register_page.register_user("David", "Blaine")
    
@pytest.mark.regression
def test_register_data8(register_page, test_logger):

    register_page.launch_app("/Register.html")
    register_page.register_user("Ben", "Affleck")