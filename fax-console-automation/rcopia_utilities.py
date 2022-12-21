from selenium.webdriver.common.by import By

# Local Libraries
from base_page import BasePage
from base_element import BaseElement


class ProductUtilitiesPage(BasePage):

    # Product Utilities Subpage

    @property
    def sig_img_approval_link(self):
        locator = (By.XPATH, "//a[text()='Signature Image Approval']")
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def enable_prescriber_link(self):
        locator = (By.XPATH, "//a[text()='Enable Prescriber for Product']")
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def enable_agent_link(self):
        locator = (By.XPATH, "//a[text()='Enable Provider Agent for Product']")
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def prescription_query_link(self):
        locator = (By.XPATH, "//a[text()='Prescription Query']")
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def fax_console_link(self):
        locator = (By.XPATH, "//a[text()='Fax Console']")
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def pharmacy_maintenance_link(self):
        locator = (By.XPATH, "//a[text()='Pharmacy Maintenance']")
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def reset_digital_sig_pass_link(self):
        locator = (By.XPATH, "//a[contains(., 'Reset Digital Signature')]")
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )
