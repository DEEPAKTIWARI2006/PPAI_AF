# import time
# import pytest
# from pages.register_page import RegisterPage
    
# @pytest.mark.flow("registration")
# @pytest.mark.test_id("TC02")
# @pytest.mark.category("regression")
# @pytest.mark.regression
# def test_register_user2(register_page, test_data):

#     register_page.launch_app("/Register.html")
#     register_page.register_user(test_data)

#     if test_data.is_success():
#         assert register_page.is_registration_successful()
#     else:
#         assert register_page.is_error_message_displayed("Invalid")
        
        