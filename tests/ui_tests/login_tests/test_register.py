import pytest
from pages.register_page import RegisterPage
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.mark.smoke
def test_register(register_page):

    register_page.launch_app("/Register.html")
    logger.info("Entering registration data")
    register_page.register_user("John", "Doe")
