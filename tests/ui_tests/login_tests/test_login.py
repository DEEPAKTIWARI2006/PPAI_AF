import time
import pytest
from pages.login_page import LoginPage
    
@pytest.mark.flow("login")
@pytest.mark.test_id("TC02")
@pytest.mark.category("smoke")
@pytest.mark.smoke
def test_user_login(login_page, test_data):

    login_page.launch_app("")
    # login_page.login_user(test_data)
    