from selenium.webdriver.common.by import By

# Local Libraries
from base_page import BasePage
from base_element import BaseElement

class companyMessaging(BasePage):

    @property
    def username_input(self):
        locator = (By.ID, 'login-email')
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def password_input(self):
        locator = (By.ID, 'login-password')
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def login_button(self):
        locator = (By.ID, 'login-button')
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def search_feeds_input(self):
        locator = (By.XPATH, '//*[@id="ng-app"]/body/div[3]/div/div[3]/div[1]/div/div[1]/div/input')
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def one_on_one_button(self):
        locator = (By.LINK_TEXT, '1-on-1')
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def groups_button(self):
        locator = (By.LINK_TEXT, 'Groups')
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def faa_group_button(self):
        locator = (By.XPATH, "//span[.='Fax Automation Alerts']")
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def send_message_input(self):
        locator = (By.CSS_SELECTOR, "textarea[ng-model='newMessageText']")
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def logout_button(self):
        locator = (By.XPATH, "//*[@id='ng-app']/body/div[1]/div/div/div[3]/a[2]")
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

