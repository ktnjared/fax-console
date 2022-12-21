from selenium.webdriver.common.by import By

# Local Libraries
from base_page import BasePage
from base_element import BaseElement


class StaffAreaLogin(BasePage):

    @property
    def username_input(self):
        locator = (By.NAME, 'username')
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def password_input(self):
        locator = (By.NAME, 'password')
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def login_button(self):
        locator = (By.CSS_SELECTOR, "input[name='submit']")
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )
