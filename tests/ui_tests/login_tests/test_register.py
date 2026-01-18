# pylint: disable=missing-function-docstring

import pytest


@pytest.mark.flow("registration")
@pytest.mark.test_id("TC01")
@pytest.mark.category("smoke")
@pytest.mark.smoke
def test_register_user(register_page, test_data):

    register_page.launch_app("/Register.html")
    register_page.register_user(test_data)
    assert register_page.is_error_message_displayed(test_data)


# # @pytest.mark.flow("registration")
# # @pytest.mark.test_id("TC01")
# # @pytest.mark.category("regression")
# # @pytest.mark.regression
# # def test_register_user_regression(register_page, test_data):

# #     register_page.launch_app("/Register.html")
#     # register_page.register_user(test_data)

#     # if test_data.is_success():
#     #     assert register_page.is_registration_successful()
#     # else:
#     #     assert register_page.is_error_message_displayed("Invalid")
