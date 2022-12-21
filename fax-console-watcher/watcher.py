# Fax Console Automation Watcher
# 
# Copyright 2019 Jared Schmidt
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
import os
import sys
import time
from pathlib import Path
from socket import gethostname

from base_page import BasePage
from messaging import companyMessaging

# ****************************************************************************
# PLATFORM
if sys.platform == 'win32':
    PLATFORM = 'win32'
elif sys.platform == 'darwin':
    PLATFORM = 'mac64'
elif sys.platform == 'linux':
    PLATFORM = 'linux64'

# ****************************************************************************
# CURRENT HOST NAME
CHN = gethostname() 

# ****************************************************************************
# PATHS
REPOPATH = os.path.join(str(Path.home()), 'source', 'repo')
FAXCONSOLEPATH = os.path.join(REPOPATH, 'fax-console')
FCAPATH = os.path.join(FAXCONSOLEPATH, 'fca')
WATCHERPATH = os.path.join(FAXCONSOLEPATH, 'watcher')
WEBDRIVERPATH = os.path.join(FAXCONSOLEPATH, 'webdriver')
LOGPATH = os.path.join(FCAPATH, 'log')

# ****************************************************************************
# Messaging Variables
msg_username = 'watcher@company.tld'
msg_chat_group = 'Fax Automation Alerts'

# move this to secrets
msg_password = 'PasswordGoesHere' 

# ****************************************************************************
# Epoch Time Variables
te_last_run = int(time.time())
te_now = int(time.time())
te_delta_threshold_min = int(30) # number of minutes FCA allowed to not run
te_delta_threshold = int(60 * te_delta_threshold_min) # unix time is given in seconds

# ****************************************************************************
# ISO 8601 Time Variables
t_iso = time.strftime('%Y-%m-%d %H:%M:%S')
tlr_iso = datetime.datetime.fromtimestamp(te_last_run).strftime('%Y-%m-%d %H:%M:%S')

# ***************************************************************************
# Get last run time for FCA in Epoch Time
with open(os.path.join(LOGPATH, 'lastrun.log'), 'r') as logfile:
    te_last_run = int(logfile.read())

# ****************************************************************************
# Update last run time ISO 8601 value
tlr_iso = datetime.datetime.fromtimestamp(te_last_run).strftime('%Y-%m-%d %H:%M:%S')

# ***************************************************************************
# Get current time in Epoch Time
te_now = int(time.time())

# ***************************************************************************
# Find last run Epoch Time delta
tu_delta = te_now - te_last_run

# ***************************************************************************
# Determine if Watcher needs to message Product group
if te_now - te_last_run > te_delta_threshold:

    # ***************************************************************************
    # Import Browser and Selenium requirements
    import requests
    import urllib3.exceptions
    from asyncio import sleep
    from requests.adapters import HTTPAdapter
    from selenium import webdriver
    from selenium.common.exceptions import NoSuchElementException, TimeoutException
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.alert import Alert
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
    from selenium.webdriver.firefox.options import Log, Options

    # ***************************************************************************
    # Browser Configuration - Google Chrome
    WEBDRIVER = 'geckodriver'

    WEBDRIVERBINPATH_ELEMENTS = [WEBDRIVER, '_', PLATFORM]
    WEBDRIVERBINPATH = ''.join(str(e) for e in WEBDRIVERBINPATH_ELEMENTS)

    if PLATFORM == 'win32':
        WEBDRIVERBIN = str(WEBDRIVER + '.exe')
    else:
        WEBDRIVERBIN = WEBDRIVER
    
    WEBDRIVERFULLPATH = os.path.join(WEBDRIVERPATH, WEBDRIVERBINPATH, WEBDRIVERBIN)
    print(WEBDRIVERFULLPATH)

    if CHN == 'JSCHMIDT2-7480':
        fx_capabilities = DesiredCapabilities().FIREFOX
        fx_capabilities["marionette"] = False

        binary = FirefoxBinary(r"C:\\Program Files\\Mozilla Firefox\\Firefox.exe") # Release Version

        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 1) # 0: Desktop, 1: default "Downloads" directory, 2: use the directory
        fp.set_preference("browser.helperApps.alwaysAsk.force", False)
        fp.set_preference("browser.download.manager.showWhenStarting", False) 
        fp.set_preference("browser.privatebrowsing.autostart", True)
        # fp.set_preference("browser.download.dir", "H:\Downloads") 

        options = Options()
        options.add_argument('-no-remote -p fca-watcher')
        
        time.sleep(10)

        browser = webdriver.Firefox(capabilities=fx_capabilities, firefox_binary=binary, firefox_profile = fp, firefox_options=options)
    
    # # Chrome on Work Laptop
    # if CHN == 'JSCHMIDT2-7480':
    #     options = webdriver.ChromeOptions()
    #     options.add_argument('--incognito --start-maximized')
    #     browser = webdriver.Chrome(WEBDRIVERFULLPATH, options=options)
    #     browser.set_window_position(-1000, 5)
    #     browser.set_window_size(800, 900)

    # # Chrome on Monitor
    # elif CHN == 'GT-MONITOR1':
    #     options = webdriver.ChromeOptions()
    #     options.add_argument("--incognito --start-maximized")
    #     browser = webdriver.Chrome(WEBDRIVERFULLPATH, options=options)
    
    # # Chrome on the Mac mini in MGR office
    # elif CHN == 'GT-Macmini.local':
    #     options = webdriver.ChromeOptions()
    #     options.add_argument("--incognito")
    #     browser = webdriver.Chrome(WEBDRIVERFULLPATH, options=options)
    #     browser.set_window_position(0, 675)
    #     browser.set_window_size(1366, 365)

    # # Chrome on a Generic computer
    # else:
    #     options = webdriver.ChromeOptions()
    #     options.add_argument("--incognito")
    #     browser = webdriver.Chrome(WEBDRIVERFULLPATH, options=options)
    #     browser.set_window_position(5, 5)
    #     browser.set_window_size(1050, 700)
    
    # ***************************************************************************
    # Akario Product URL
    url_elements = ['https://', 'product.company.tld/', '#/login']
    BasePage.url = ''.join(str(e) for e in url_elements)

    # ***************************************************************************
    # Open Product Login Page
    product_page = companyMessaging(driver=browser)
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=3)
    session.mount('https://', adapter)
    attempts = 0
    quit_watcher = None

    while attempts < 3:
        try:
            request = session.get(BasePage.url)
            request.raise_for_status()
            quit_watcher = False
            break
        except (http.client.RemoteDisconnected,
                requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
                urllib3.exceptions.ProtocolError) as err:
            attempts += 1
            quit_watcher = True
            sleep(10)

    if quit_watcher is True:
        exit()
    else:
        product_page.go()

    # ***************************************************************************
    # Log into Product
    try:
        product_page.username_input.input_text(msg_username)
    except NoSuchElementException as err:
        exit()

    try:
        product_page.password_input.input_text(msg_password)
    except NoSuchElementException as err:
        exit()

    product_page.login_button.click()

    # ***************************************************************************
    # Select Correct Chat Feed
    product_page.groups_button.click()
    product_page.search_feeds_input.input_text(msg_chat_group)
    product_page.faa_group_button.click()

    # ***************************************************************************
    # Write in Text Box
    # product_page.send_message_input.input_text('Notice: Fax Console Automation has not run since ')
    # product_page.send_message_input.input_text(tlr_iso)
    # product_page.send_message_input.input_text('.')
    # product_page.send_message_input.input_text(Keys.RETURN)


    # ***************************************************************************
    # Press keystroke for Logout
    logout = ActionChains(driver=browser)
    logout.send_keys(Keys.CONTROL + Keys.SHIFT + 'L')
    logout.perform()

    # ***************************************************************************
    # Click Yes to Log Out
    try:
        if "Yes" in product_page.logout_button.text:
            product_page.logout_button.click()
    except NoSuchElementException as err:
        exit()
    
    # ***************************************************************************
    # Close Browser
    browser.close()

# ****************************************************************************
# Exit Fax Console Automation Watcher
quit()
