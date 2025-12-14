import pytest
from pages.register_page import RegisterPage

@pytest.mark.smoke
def test_register_data1(register_page):

    register_page.launch_app("/Register.html")
    register_page.register_user("Vivaan", "Tiwari")
    assert register_page.is_error_message_displayed("Invalid username or password")

@pytest.mark.smoke
def test_register_data2(register_page, test_logger):

    register_page.launch_app("/Register.html")
    register_page.register_user("Sunil", "Kumar")
    
    
@pytest.mark.smoke
def test_register_data3(register_page, test_logger):

    register_page.launch_app("/Register.html")
    register_page.register_user("Alex", "Cruz")
    
@pytest.mark.smoke
def test_register_data4(register_page, test_logger):

    register_page.launch_app("/Register.html")
    register_page.register_user("Ajay", "Sharma")