from selenium.webdriver.common.by import By

# Local Libraries
from base_page import BasePage
from base_element import BaseElement


class StaffOptionsPage(BasePage):

    # Initial Staff Area Page after Login

    @property
    def smx_utilities_link(self):
        locator = (By.XPATH, "//a[text()='SMX Utilities']")
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def product_utilities_link(self):
        locator = (By.XPATH, "//a[text()='Product Utilities']")
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def account_maintenance_link(self):
        locator = (By.XPATH, "//a[text()='Account Maintenance']")
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )
    @property
    def report_link(self):
        locator = (By.XPATH, "//a[text()='Report']")
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def logout_link(self):
        locator = (By.XPATH, "//a[text()='Log out']")
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )
