from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

# Local Libraries
from base_page import BasePage
from base_element import BaseElement


class FaxConsolePage(BasePage):

    # Fax Console Page

    @property
    def faxcon_back_to_staff_area_butn(self):
        locator = (By.XPATH, "//a[contains(@href,'staff.StaffHome')]/img")
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def faxcon_menu_status(self):
        locator = (By.CSS_SELECTOR, "select[name='s_status']")
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    def faxcon_menu_status_set_failed(self):
        search_status_menu = self.driver.find_element_by_css_selector("select[name='s_status']")
        search_status_sel = Select(search_status_menu)
        search_status_sel.select_by_value("F")
        return None

    @property
    def faxcon_fax_date(self):
        locator = (By.NAME, 's_fax_date')
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    # def faxcon_table(self):
    #     locator = (By.XPATH, "//a[text()='Fax Sub ID / Type']/../../..")
    #     return BaseElement(
    #         self.driver,
    #         by=locator[0],
    #         value=locator[1]
    #     )

    def faxcon_table_header(self):
        locator = (By.XPATH, "//a[text()='Fax Sub ID / Type']/../..")
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )

    @property
    def faxcon_search_butn(self):
        locator = (By.CSS_SELECTOR, "input[name='search']")
        return BaseElement(
            self.driver,
            by=locator[0],
            value=locator[1]
        )
