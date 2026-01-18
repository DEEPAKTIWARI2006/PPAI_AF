class RegisterLocators:

    FIRST_NAME = ("role", "textbox", {"name": "First Name"})
    LAST_NAME = ("role", "textbox", {"name": "Last Name"})
    ADDRESS = ("xpath", "//textarea[@ng-model='Adress']")
    EMAIL = ("xpath", "//input[@ng-model='EmailAdress']")
    PHONE = ("xpath", "//input[@ng-model='Phone']")
    GENDER = ("role", "radio", {"name": "{gender}", "exact": True})
    HOBBY = ("xpath", "//input[@value='{hobby}']")
    LANGUAGE_DROPDOWN = ("css", "#msdd")
    FORM_BODY = ("css", "#basicBootstrapForm")
    LANGUAGE_OPTION_BY_TEXT = ("text", "{language}")
    SKILLS_SELECT = ("css", "#Skills")
    COUNTRY_SEARCH = (
        "xpath",
        "//span[@role='combobox' and contains(@aria-labelledby, 'country')]",
    )
    COUNTRY_OPTION_BY_NAME = ("role", "treeitem", {"name": "{country}"})
    COUNTRY_WITH_ERROR = ("css", "#countries")
    DOB_YEAR_SELECT = ("css", "#yearbox")
    DOB_MONTH_SELECT = ("xpath", "//select[@placeholder='Month']")
    DOB_DAY_SELECT = ("css", "#daybox")
    PASSWORD = ("css", "#firstpassword")
    CONFIRM_PASSWORD = ("css", "#secondpassword")
    SUBMIT_BUTTON = ("role", "button", {"name": "Submit"})
    ERROR_MESSAGE_BY_TEXT = ("text", "{error_text}")
