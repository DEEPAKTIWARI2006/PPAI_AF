class RegisterLocators:
    FIRST_NAME = "//input[@placeholder='First Name']"
    LAST_NAME = "//input[@placeholder='Last Name']"
    SUBMIT_BUTTON = "//BUTTON[@TYPE='submit']"
    
    # 🔹 Dynamic locators
    ERROR_MESSAGE_BY_TEXT = "//span[contains(text(), '{error_text}')]"
    DROPDOWN_OPTION_BY_TEXT = "//li[normalize-space()='{option}']"

    
