# Fax Console Automation
#
# Copyright 2018 Jared Schmidt
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datetime
import http.client
import logging.handlers
import os
import requests
import sys
import time
import urllib3.exceptions
from datetime import date, timedelta
from pathlib import Path
from requests.adapters import HTTPAdapter
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from socket import gethostname

# Local Libraries
from base_page import BasePage
from fax_console import FaxConsolePage
from product_utilities import ProductUtilitiesPage
from staff_area import StaffAreaLogin
from staff_options import StaffOptionsPage

################################################################################
# ARE WE RUNNING AGAINST PRODUCTION?
IS_PROD = True

# Region Variables
if IS_PROD is True:
    region_hostname = ['pd1.prod', 'pd2.prod', 'pd3.prod', 'pd4.prod']
    region_username = ['fcauserpd1', 'fcauserpd2', 'fcauserpd3', 'fcauserpd4']
    region_name = ['REGION1', 'REGION2', 'REGION3', 'REGION4']
    region_db = ['PD1', 'PD2', 'PD3', 'PD4']
    region_rx_code = ['AA', 'BB', 'CC', 'DD']
else:
    region_hostname = ['ct1.staging', 'ct2.staging', 'dm1.demo']
    region_username = ['fcauserct1', 'fcauserct2', 'fcauserdm1']
    region_name = ['STAGING1', 'STAGING2', 'DEMO']
    region_db = ['CT1', 'CT2', 'DM1']
    region_rx_code = ['SA', 'SB', 'DM']

# Region Array Lists
if IS_PROD is True:
    # Region 1: 0
    # Region 2: 1
    # Region 3: 2
    # Region 4: 3
    array_list = [0, 1, 2, 3]
else:
    # Staging 1: 0
    # Staging 2: 1
    # Demo     : 2
    array_list = [0, 1, 2]

################################################################################
# OS PLATFORM
if sys.platform == 'win32':
    PLATFORM = 'win32'
elif sys.platform == 'darwin':
    PLATFORM = 'mac64'
elif sys.platform == 'linux':
    PLATFORM = 'linux64'

################################################################################
# SCRIPT HOST DETAILS

# NAME
COMPUTERNAME = gethostname()

# SCRIPT PATHS
REPOPATH = os.path.join(str(Path.home()), 'Source', 'Repo')
FAXCONSOLEPATH = os.path.join(REPOPATH, 'fax-console')
FCAPATH = os.path.join(FAXCONSOLEPATH, 'fca')
WATCHERPATH = os.path.join(FAXCONSOLEPATH, 'watcher')
WEBDRIVERPATH = os.path.join(FAXCONSOLEPATH, 'webdriver')
LOGPATH = os.path.join(FCAPATH, 'log')

# BROWSER CONFIGURATION - GOOGLE CHROME
WEBDRIVER = 'chromedriver'

WEBDRIVERBINPATH_ELEMENTS = [WEBDRIVER, '_', PLATFORM]
WEBDRIVERBINPATH = ''.join(str(e) for e in WEBDRIVERBINPATH_ELEMENTS)

if PLATFORM == 'win32':
    WEBDRIVERBIN = str(WEBDRIVER + '.exe')
else:
    WEBDRIVERBIN = WEBDRIVER

WEBDRIVERFULLPATH = os.path.join(WEBDRIVERPATH, WEBDRIVERBINPATH, WEBDRIVERBIN)

# CHROME ON WORK LAPTOP
if COMPUTERNAME == 'WORK-LAPTOP':
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    browser = webdriver.Chrome(WEBDRIVERFULLPATH, options=options)
    browser.set_window_position(-1200, 5)
    browser.set_window_size(1000, 900)

# CHROME ON APO MONITOR
elif COMPUTERNAME == 'MONITOR':
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito --start-maximized")
    browser = webdriver.Chrome(WEBDRIVERFULLPATH, options=options)

# CHROME ON THE MAC MINI IN MGR OFFICE
elif COMPUTERNAME == 'Macmini':
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    browser = webdriver.Chrome(WEBDRIVERFULLPATH, options=options)
    browser.set_window_position(0, 675)
    browser.set_window_size(1366, 365)

# CHROME ON A GENERIC COMPUTER
else:
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    browser = webdriver.Chrome(WEBDRIVERFULLPATH, options=options)
    browser.set_window_position(5, 5)
    browser.set_window_size(1050, 700)

################################################################################
#
# ########    ###    ##     ##                                                                
# ##         ## ##    ##   ##                                                                 
# ##        ##   ##    ## ##                                                                  
# ######   ##     ##    ###                                                                   
# ##       #########   ## ##                                                                  
# ##       ##     ##  ##   ##                                                                 
# ##       ##     ## ##     ##                                                                
#
#  ######   #######  ##    ##  ######   #######  ##       ########                            
# ##    ## ##     ## ###   ## ##    ## ##     ## ##       ##                                  
# ##       ##     ## ####  ## ##       ##     ## ##       ##                                  
# ##       ##     ## ## ## ##  ######  ##     ## ##       ######                              
# ##       ##     ## ##  ####       ## ##     ## ##       ##                                  
# ##    ## ##     ## ##   ### ##    ## ##     ## ##       ##                                  
#  ######   #######  ##    ##  ######   #######  ######## ########                            
#
#    ###    ##     ## ########  #######  ##     ##    ###    ######## ####  #######  ##    ## 
#   ## ##   ##     ##    ##    ##     ## ###   ###   ## ##      ##     ##  ##     ## ###   ## 
#  ##   ##  ##     ##    ##    ##     ## #### ####  ##   ##     ##     ##  ##     ## ####  ## 
# ##     ## ##     ##    ##    ##     ## ## ### ## ##     ##    ##     ##  ##     ## ## ## ## 
# ######### ##     ##    ##    ##     ## ##     ## #########    ##     ##  ##     ## ##  #### 
# ##     ## ##     ##    ##    ##     ## ##     ## ##     ##    ##     ##  ##     ## ##   ### 
# ##     ##  #######     ##     #######  ##     ## ##     ##    ##    ####  #######  ##    ## 

################################################################################
# VARIABLES

# CONSOLE LOG
# USE: To add data into the log file, use log.info() instead of print().
CONSOLELOG = os.path.join(LOGPATH, 'console.log')

# Log Format
LOGGING_LEVEL = logging.DEBUG
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')

# Handler to output data to log file
handler = logging.handlers.RotatingFileHandler(
    CONSOLELOG, mode='a', maxBytes=5000000, backupCount=19)
handler.setFormatter(formatter)

# Handler to output data to the console
cli = logging.StreamHandler(sys.stdout)
cli.setFormatter(formatter)
cli.setLevel(LOGGING_LEVEL)

log = logging.getLogger("FaxConsole")
log.addHandler(handler)
log.addHandler(cli)
log.setLevel(LOGGING_LEVEL)

# Number of days to run against
days_back_to_run = 10
seconds_back_to_run = (days_back_to_run - 1) * 86400

# Define Day Markers
today = date.today()
daymargin = timedelta(seconds=86400)
loop_start_date = today - timedelta(seconds=seconds_back_to_run)
loop_end_date = today + daymargin

################################################################################
# Begin Region Loop
for i in array_list:

    # Setup Loop for Running Multiple Days
    t_date = loop_start_date

    t_yy = t_date.year
    t_mm = t_date.month
    t_dd = t_date.day

    date_elements = [t_mm, t_dd, t_yy]
    t_date_printable = '/'.join(str(e) for e in date_elements)

    # Additional Logging Details
    rgn_name = region_name[i]
    if region_name[i] == region_name[-1]:
        rgn_next_name = region_name[0]
    else:
        rgn_next_name = region_name[i + 1]
    rgn = rgn_name + ': '

    # Build Product Staff Area URL
    url_elements = ['https://', region_hostname[i], '.company.tld/staff/stafflogin.jsp']
    BasePage.url = ''.join(str(e) for e in url_elements)

    ################################################################################
    # Staff Area Login
    ################################################################################
    staff_login_page = StaffAreaLogin(driver=browser)
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=3)
    session.mount('https://', adapter)
    log.info(rgn + 'Connecting to ' + BasePage.url + '.')
    attempts = 0
    skip_to_next_region = None

    while attempts < 3:
        try:
            request = session.get(BasePage.url)
            request.raise_for_status()
            skip_to_next_region = False
            log.info(rgn + "Connection established.")
            break
        except (http.client.RemoteDisconnected,
                requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
                urllib3.exceptions.ProtocolError) as err:
            log.info(rgn + str(err))
            log.info(
                rgn + "Unable to establish connection during attempt " + attempts + ".")
            log.info(rgn + "Retrying connection in 10 seconds.")
            attempts += 1
            skip_to_next_region = True
            time.sleep(10)

    if skip_to_next_region is True:
        log.info("Unable to establish connection to " + rgn_name + ".")
        log.info(rgn + "Moving on to " + rgn_next_name + ".")
        continue
    else:
        staff_login_page.go()

    # Enter the username
    try:
        staff_login_page.username_input.input_text(region_username[i])
    except TimeoutException as err:
        log.info(str(err))
        log.info(rgn + "Unable to locate username textbox.")
        log.info(rgn + "Moving on to " + rgn_next_name + ".")
        continue

    # Enter the password
    try:
        staff_login_page.password_input.input_text('********')
    except TimeoutException as err:
        log.info(str(err))
        log.info(rgn + "Unable to enter password.")
        log.info(rgn + "Moving on to " + rgn_next_name + ".")
        continue

    # Assert that the Login button exists otherwise move on to the next region
    try:
        assert staff_login_page.login_button.attribute('value') == 'Login'
        staff_login_page.login_button.click()
    except AssertionError as err:
        log.info(str(err))
        log.info(rgn + "Unable to click on the Login button.")
        log.info(rgn + "Moving on to " + rgn_next_name + ".")
        continue

    ################################################################################
    # Staff Options Page
    ################################################################################
    staff_options_page = StaffOptionsPage(driver=browser)

    # Click the Rcopia Utilities link
    try:
        staff_options_page.rcopia_utilities_link.click()
    except TimeoutException as err:
        log.info(str(err))
        log.info(rgn + "Unable to locate Rcopia Utilities link.")
        log.info(rgn + "Moving on to " + rgn_next_name + ".")
        continue

    ################################################################################
    # Rcopia Utilities Page
    ################################################################################
    rcopia_utilities_page = RcopiaUtilitiesPage(driver=browser)

    # Click the Fax Console link
    try:
        rcopia_utilities_page.fax_console_link.click()
    except TimeoutException as err:
        log.info(str(err))
        log.info(rgn + "Unable to locate Fax Console link.")
        log.info(rgn + "Moving on to " + rgn_next_name + ".")
        continue

        # Begin Date Loop
    while t_date >= loop_start_date and t_date < loop_end_date:

        print("Started running against " + str(t_date) + ".")

        t_yy = t_date.year
        t_mm = t_date.month
        t_dd = t_date.day

        date_elements = [t_mm, t_dd, t_yy]
        t_date_printable = '/'.join(str(e) for e in date_elements)

        ################################################################################
        # Fax Console Main Page
        ################################################################################

        fax_console_page = FaxConsolePage(driver=browser)

        # Select the Fax Date box
        fax_date_default_value = fax_console_page.faxcon_fax_date.attribute('value')
        fax_date_default_value_len = len(fax_date_default_value)

        # Clear the Fax Date box
        for l in range(1, fax_date_default_value_len + 1):
            fax_console_page.faxcon_fax_date.input_text(Keys.ARROW_LEFT)

        for l in range(1, fax_date_default_value_len + 1):
            fax_console_page.faxcon_fax_date.input_text(Keys.DELETE)

        # Enter t_date_printable into Fax Date box
        fax_console_page.faxcon_fax_date.input_text(t_date_printable)

        # Set Status dropdown to Failed
        try:
            fax_console_page.faxcon_menu_status_set_failed()
            log.info(rgn + "Status successfully changed to 'Failed'.")
        except TimeoutException as err:
            log.info(str(err))
            log.info(rgn + "Unable to locate Status dropdown.")
            log.info(rgn + "Moving on to " + rgn_next_name + ".")
            continue

        # Search for Results
        try:
            fax_console_page.faxcon_search_butn.click()
        except TimeoutException as err:
            log.info(str(err))
            log.info(rgn + "Unable to locate Fax Console Search button.")
            log.info(rgn + "Moving on to " + rgn_next_name + ".")
            continue

        ################################################################################
        ################################################################################
        ################################################################################
        #
        # Everything below this point needs to be moved to classes. It's a mess.
        # Unfortunately, leadership does not care about my mess because it works,
        # so there's no time to allocate to it.
        #
        ################################################################################
        ################################################################################
        ################################################################################

        # Find the table that the prescriptions are located in and get row count
        try:
            faxconsole_table = browser.find_element_by_xpath("/html/body/form[2]/table[2]/tbody")
            faxcon_rx_rows = len(faxconsole_table.find_elements_by_tag_name('tr')) - 1
        except NoSuchElementException as err:
            log.info(str(err))
            log.info(rgn + "Unable to locate table of prescriptions.")
            log.info(rgn + "Moving on to " + rgn_next_name + ".")
            continue

        ################################################################################
        # Take Action on Each Fax in Environment
        ################################################################################
        while faxcon_rx_rows > 0:

            ################################################################################
            # Find the first prescription in the table
            ################################################################################

            # Check that first header == 'Fax Sub ID / Type'
            try:
                faxcon_header_col1 = browser.find_element_by_xpath("/html/body/form[2]/table[2]/tbody/tr[1]/th[1]/a")
                faxcon_header_col1_name = faxcon_header_col1.text
            except (NoSuchElementException, TimeoutException) as err:
                log.info(str(err))
                log.info(
                    rgn + "Unable to locate table of prescriptions header column 1.")
                log.info(rgn + "Moving on to " + rgn_next_name + ".")
                continue

            try:
                assert faxcon_header_col1_name == 'Fax Sub ID / Type'
            except AssertionError as err:
                log.info(str(err))
                log.info(rgn + "Header column 1 does not have the correct text.")
                log.info(rgn + "Moving on to " + rgn_next_name + ".")
                continue

            # Check that second header == 'Rx ID/Tran ID'
            try:
                faxcon_header_col2 = browser.find_element_by_xpath("/html/body/form[2]/table[2]/tbody/tr[1]/th[2]/a")
            except (NoSuchElementException, TimeoutException) as err:
                log.info(str(err))
                log.info(
                    rgn + "Unable to locate table of prescriptions header column 2.")
                log.info(rgn + "Moving on to " + rgn_next_name + ".")
                continue

            faxcon_header_col2_name = faxcon_header_col2.text
            try:
                assert faxcon_header_col2_name == 'Rx ID/Tran ID'
            except AssertionError as err:
                log.info(str(err))
                log.info(rgn + "Header column 2 does not have the correct text.")
                log.info(rgn + "Moving on to " + rgn_next_name + ".")
                continue

            # Get hidden value of rx_id_xxxxxxxxxx value = rx_id
            try:
                faxcon_rx1_col1 = browser.find_element_by_xpath("/html/body/form[2]/table[2]/tbody/tr[2]/td[1]/input[2]")
            except (NoSuchElementException, TimeoutException) as err:
                log.info(str(err))
                log.info(rgn + "Unable to locate hidden prescription ID in column 1.")
                log.info("Exiting automation and quitting browser. Will attempt to deal with this on next run.")
                browser.close()
                quit()

            try:
                faxcon_rx1_col1_id = faxcon_rx1_col1.get_attribute("value")
                log.info(rgn + "Found value. We think the prescription ID is " + faxcon_rx1_col1_id + ".")
            except (NoSuchElementException, TimeoutException) as err:
                log.info(str(err))
                log.info(rgn + "Unable to locate a value.")
                log.info(rgn + "Moving on to " + rgn_next_name + ".")
                continue

            # Compare 'RX: XX-' + rx_id is the same
            try:
                faxcon_rx1_col2 = browser.find_element_by_xpath("/html/body/form[2]/table[2]/tbody/tr[2]/td[2]/a")
                rx_serial = faxcon_rx1_col2.text
            except (NoSuchElementException, TimeoutException) as err:
                log.info(str(err))
                log.info(rgn + "Unable to locate prescription serial number on page.")
                log.info(rgn + "Moving on to " + rgn_next_name + ".")
                continue

            try:
                assert 'RX: ' + region_rx_code[i] + '-' + faxcon_rx1_col1_id == rx_serial
                log.info(rgn + "Successfully located prescription " + rx_serial + ".")
                log.info(rgn + "Begin processing of " + rx_serial + ".")
            except AssertionError as err:
                log.info(str(err))
                log.info(rgn + rx_serial + " and " +
                            region_rx_code[i] + '-' + faxcon_rx1_col1_id + " do not match.")
                log.info("Aborting automation on this prescription.")
                continue

            ################################################################################
            # Begin processing of current individual prescription
            ################################################################################

            # Make readable variables that now make sense for prescription actions.
            rx_id = faxcon_rx1_col1_id
            rx_link = faxcon_rx1_col2
            rx_log = rgn + rx_serial + ": "

            # Verify Prescription Status is actually 'F -'
            try:
                faxcon_rx1_col3 = browser.find_element_by_xpath("/html/body/form[2]/table[2]/tbody/tr[2]/td[3]")
                rx_status = faxcon_rx1_col3.text
            except (NoSuchElementException, TimeoutException) as err:
                log.info(str(err))
                log.info(rx_log + "Unable locate prescription status.")
                log.info(rx_log + "Aborting automation on this prescription.")
                continue

            try:
                assert rx_status[:3] == "F -"
                log.info(rx_log + "Prescription status is 'F'.")
            except AssertionError as err:
                log.info(str(err))
                log.info(rx_log + "Prescription status is not 'F -'.")
                log.info(rx_log + "Aborting automation on this prescription.")
                continue

            # Click the prescription link in the first row
            try:
                rx_link.click()
                log.info(rx_log + "Launching Fax Action Log page.")
            except (NoSuchElementException, TimeoutException) as err:
                log.info(str(err))
                log.info(rx_log + "Unable to click on prescription link.")
                log.info(rx_log + "Aborting automation on this prescription.")
                continue

            # Assign variables for the multiple tabs now that they exist
            try:
                tab_faxconsole = browser.window_handles[0]
            except (NoSuchElementException, TimeoutException) as err:
                log.info(str(err))
                log.info(rx_log + "Unable to assign the primary tab variable.")
                log.info(rx_log + "Abort all automation!")
                break

            try:
                tab_faxactionlog = browser.window_handles[1]
            except (NoSuchElementException, TimeoutException) as err:
                log.info(str(err))
                log.info(rx_log + "Unable to assign the Fax Action Log tab variable.")
                log.info(rx_log + "Aborting automation on this prescription.")
                continue

            ################################################################################
            # Fax Action Log tab
            ################################################################################

            # Switch to Fax Action Log tab
            try:
                browser.switch_to.window(tab_faxactionlog)
            except (NoSuchElementException, TimeoutException) as err:
                log.info(str(err))
                log.info(rx_log + "Unable to switch to Fax Action Log tab.")
                log.info(rx_log + "Aborting automation on this prescription.")
                continue
            # print(browser.title)

            # Fax Action Log tab
            # This page is extremely poorly written for automation.
            # Verify that we are on the correct page
            try:
                assert browser.title == "Fax Action Log"
                log.info(rx_log + "ASSERT: Fax Action Log page title confirmed.")
            except AssertionError as err:
                log.info(str(err))
                log.info(
                    rx_log + "ASSERT FAILED: Unable to confirm that the Fax Action Log page has loaded.")
                log.info(rx_log + "Aborting automation on this prescription.")
                continue

            # Check/Require that an H3 with Pending Prescription or Archive Prescription exists on the page.
            #
            # OLD WAY:
            # fal_title_words = ['Pending Prescription ', 'Archived Prescription ']
            # conditions = " or ".join(["contains(., '%s')" % keyword for keyword in fal_title_words])
            # expression = "//h3[%s]" % conditions
            # rx_action_log_title = browser.find_element_by_xpath(expression)
            #
            # NEW WAY:
            try:
                rx_action_log_title = browser.find_element_by_xpath("//h3["
                                                                    "contains(., 'Pending Prescription ')"
                                                                    " or "
                                                                    "contains(., 'Archived Prescription ')"
                                                                    "]")
                log.info(rx_log + "Fax Action Log page title confirmed.")
            except NoSuchElementException as err:
                log.info(str(err))
                log.info(rx_log + "Unable to locate a Fax Action Log page title.")
                log.info(rx_log + "Aborting automation on this prescription.")
                continue

            try:
                assert rx_id in rx_action_log_title.text
                log.info(
                    rx_log + "ASSERT: The correct Fax Action Log page has been opened.")
            except AssertionError as err:
                log.info(str(err))
                log.info(
                    rx_log + "ASSERT FAILED: Unable to confirm the correct Fax Action Log page has been opened.")
                log.info(rx_log + "Aborting automation on this prescription.")
                continue

            try:
                bullet_serial = browser.find_element_by_xpath("//li[contains(text(), 'Serial Number: ')]")
                log.info(rx_log + "Prescription ID has been located on Fax Action Log page.")
            except NoSuchElementException as err:
                log.info(str(err))
                log.info(rx_log + "Unable to confirm prescription ID on Fax Action Log page.")
                log.info(rx_log + "Aborting automation on this prescription.")
                continue

            try:
                assert rx_id in bullet_serial.text
                log.info(rx_log + "ASSERT: Prescription ID has been confirmed.")
            except AssertionError as err:
                log.info(str(err))
                log.info(rx_log + "ASSERT FAILED: Prescription ID cannot be confirmed.")
                log.info(rx_log + "Aborting automation on this prescription.")
                continue

            # Determine which elements exist on the page.
            # Pending Prescription
            try:
                browser.find_element_by_xpath("//h3[contains(., 'Pending Prescription ')]")
                pending_prescription = browser.find_element_by_xpath("//h3[contains(., 'Pending Prescription ')]")
            except Exception as err:
                pending_prescription = None

            # Fax failed
            try:
                browser.find_element_by_xpath("*[contains(., 'The fax server returned this error:')]")
                status_fax_failed = browser.find_element_by_xpath("*[contains(., 'The fax server returned this error:')]")
                log.info(rx_log + "Attempted fax FAILED.")
            except Exception as err:
                status_fax_failed = None

            # status:Failed(
            try:
                browser.find_element_by_xpath("*[contains(., 'status:Failed(')]")
                status_fax_action_failed = browser.find_element_by_xpath("*[contains(., 'status:Failed(')]")
                log.info(rx_log + "Fax Status: FAILED.")
            except Exception as err:
                status_fax_action_failed = None

            # status:Failed(Normal busy)
            try:
                browser.find_element_by_xpath("*[contains(., 'status:Failed('Normal busy')]")
                status_fax_action_busy = browser.find_element_by_xpath("*[contains(., 'status:Failed('Normal busy')]")
                log.info(rx_log + "Fax Status: NORMAL BUSY.")
            except Exception as err:
                status_fax_action_busy = None

            # Prescription was sent electronically using system NDC_SS.
            try:
                browser.find_element_by_xpath("*[contains(., ""'Prescription was sent electronically using system NDC_SS.')]")
                status_ndc_ss = browser.find_element_by_xpath("*[contains(., 'Prescription was sent electronically using system NDC_SS.')]")
                log.info(rx_log + "Prescription sent by NDC_SS.")
            except Exception as err:
                status_ndc_ss = None

            # Status: No verify recived, faxed
            try:
                browser.find_element_by_xpath("*[contains(., 'Status: No verify recived, faxed')]")
                status_no_verify_faxed = browser.find_element_by_xpath("*[contains(., 'Status: No verify recived, faxed')]")
                log.info(rx_log + "No verify received, so Faxed.")
            except Exception as err:
                status_no_verify_faxed = None

            # Verified
            try:
                browser.find_element_by_xpath("*[contains(., 'Verified')]")
                status_verified = browser.find_element_by_xpath("*[contains(., 'Verified')]")
                log.info(rx_log + "Prescription is marked verified.")
            except Exception as err:
                status_verified = None

            # voided
            try:
                browser.find_element_by_xpath("*[contains(., 'voided')]")
                status_voided = browser.find_element_by_xpath("*[contains(., 'voided')]")
                log.info(rx_log + "Prescription has been marked voided.")
            except Exception as err:
                status_voided = None

            # Determine which action needs to be taken
            fax_action_type = None

            if pending_prescription is not None:
                fax_action_type = 'Mark Undeliverable'
            elif status_fax_action_busy is not None:
                fax_action_type = 'Refax'
            elif status_voided is not None and ((status_fax_failed is not None) or (status_fax_action_failed is not None)):
                # fax_action_type = 'Complete'
                # Changed from Complete to Mark Undeliverable per ***** on 2018-09-12
                # Changed from Mark Undeliverable to Complete per ***** on 2019-08-29
                fax_action_type = 'Complete'
            elif status_voided is not None:
                fax_action_type = 'Complete'
            elif status_ndc_ss is not None and ((status_verified is not None) or (status_no_verify_faxed is not None)):
                fax_action_type = 'Complete'
            elif status_ndc_ss is not None and status_fax_action_failed is not None:
                fax_action_type = 'Mark Undeliverable'
            elif status_fax_failed is not None and status_fax_action_failed is not None:
                fax_action_type = 'Mark Undeliverable'
            elif status_fax_action_failed is not None:
                fax_action_type = 'Mark Undeliverable'

            log.info(rx_log + "Review determined that we need to click the " + fax_action_type + " button.")

            # Close Tab
            browser.close()
            browser.switch_to.window(tab_faxconsole)

            # Verify our prescription is still the first one listed
            try:
                assert 'RX: ' + region_rx_code[i] + '-' + rx_id == browser.find_element_by_xpath("/html/body/form[2]/table[2]/tbody/tr[2]/td[2]/a").text
                log.info(rx_log + "ASSERT: Verified " + rx_serial + " is still listed as the first prescription.")
            except AssertionError as err:
                log.info(str(err))
                log.info(rx_log + "ASSERT FAILED: " + rx_serial + " is not the first prescription in the list.")
                log.info(rx_log + "Aborting automation on this prescription.")
                continue

            # Click the checkbox for the first row item
            try:
                assert rx_id == browser.find_element_by_xpath("/html/body/form[2]/table[2]/tbody/tr[2]/td[1]/input[2]").get_attribute("value")
            except AssertionError as err:
                log.info(str(err))
                log.info(rx_log + "ASSERT FAILED: Unable to locate prescription ID")
                log.info(rx_log + "Aborting automation on this prescription.")
                continue

            try:
                rx_checkbox = browser.find_element_by_xpath("/html/body/form[2]/table[2]/tbody/tr[2]/td[1]/input[1]")
            except NoSuchElementException as err:
                log.info(str(err))
                log.info(rx_log + "")
                log.info(rx_log + "Aborting automation on this prescription.")
                continue

            rx_checkbox.click()

            # Find Buttons
            # REFAX BUTTON
            try:
                refax_butn_href = browser.find_element_by_xpath("/html/body/form[2]/table[1]/tbody/tr/td[1]/a[1]").get_attribute("href")
                if "refax" in refax_butn_href:
                    refax_butn = browser.find_element_by_xpath("/html/body/form[2]/table[1]/tbody/tr/td[1]/a[1]")
            except:
                refax_butn_href = None

            complete_butn = None
            complete_butn_href = None

            try:
                complete_butn_href = browser.find_element_by_xpath("/html/body/form[2]/table[1]/tbody/tr/td[1]/a[2]").get_attribute("href")
                if "update_status" in complete_butn_href:
                    complete_butn = browser.find_element_by_xpath("/html/body/form[2]/table[1]/tbody/tr/td[1]/a[2]")
            except NoSuchElementException as err:
                log.info(str(err))
                log.info(rx_log + "")
                log.info(rx_log + "Aborting automation on this prescription.")
                continue

            undeliverable_butn = None
            undeliverable_butn_href = None

            try:
                undeliverable_butn_href = browser.find_element_by_xpath("/html/body/form[2]/table[1]/tbody/tr/td[1]/a[3]").get_attribute("href")
                if "undeliverable" in undeliverable_butn_href:
                    undeliverable_butn = browser.find_element_by_xpath("/html/body/form[2]/table[1]/tbody/tr/td[1]/a[3]")
            except NoSuchElementException as err:
                log.info(str(err))
                log.info(rx_log + "")
                log.info(rx_log + "Aborting automation on this prescription.")
                continue

            ######################################################
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
            # DANGER THIS IS WHERE THE MAGIC HAPPENS TO MARK FAX #
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
            ######################################################

            # Click the action button
            if "Undeliverable" in fax_action_type:
                undeliverable_butn.click()
                Alert(browser).accept()
            elif "Complete" in fax_action_type:
                complete_butn.click()
            elif "Refax" in fax_action_type:
                refax_butn.click()

            # Click accept within the Alert that appears.
            if "Undeliverable" in fax_action_type:
                log.info(rx_log + "Prescription has been marked UNDELIVERABLE.")
            elif "Refax" in fax_action_type:
                log.info(rx_log + "Prescription has been REFAXED.")
            elif "Complete" in fax_action_type:
                log.info(rx_log + "Prescription has been marked COMPLETED.")

            # Update the now current row count
            try:
                faxconsole_table = browser.find_element_by_xpath("/html/body/form[2]/table[2]/tbody")
                faxcon_rx_rows = len(faxconsole_table.find_elements_by_tag_name('tr')) - 1
            except NoSuchElementException as err:
                log.info(str(err))
                log.info(rgn + "Unable to locate table of prescriptions.")
                log.info(rgn + "Moving on to " + rgn_next_name + ".")
                continue

        today = date.today()

        # Increment t_date for next loop
        t_date = t_date + timedelta(days=1)

    ################################################################################
    # Properly log out of current region
    ################################################################################
    try:
        fax_console_page.faxcon_back_to_staff_area_butn.click()
        log.info(rgn + "Logout of Fax Console was successful.")
    except TimeoutException as err:
        log.info(str(err))
        log.info(rgn + "Unable to locate the Back to Staff Area button.")
        log.info(rgn + "Moving on to " + rgn_next_name + ".")
        continue

    try:
        staff_options_page.logout_link.click()
        log.info(rgn + "Logout of Staff Area was successful.")
    except TimeoutException as err:
        log.info(str(err))
        log.info(rgn + "Unable to locate the Logout link.")
        log.info(rgn + "Moving on to " + rgn_next_name + ".")
        continue

    ################################################################################
    # Log completed activity on region
    ################################################################################
    log.info(rgn + "Automation of " + rgn_name + " has been completed.")
    if region_name[i] == region_name[-1]:
        log.info("Ending single loop of automation.")
    else:
        log.info(rgn + "Moving on to " + rgn_next_name + ".")

################################################################################
# Write log file to BASEPATH/log when completed with timestamp.
################################################################################
# If the file already exists, it will be overwritten with the latest timestamp.
timestamp = str(int(time.time()))
with open(os.path.join(LOGPATH, 'lastrun.log'), 'w') as outf:
    outf.write(timestamp)

################################################################################
# End Automation
################################################################################
browser.close()

################################################################################
# Exit Fax Console Automation
quit()
