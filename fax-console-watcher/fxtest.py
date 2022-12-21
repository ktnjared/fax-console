from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options

binary = FirefoxBinary("/Applications/Firefox.app")

capabilities = webdriver.DesiredCapabilities().FIREFOX
capabilities["marionette"] = False

options = Options()
options.add_argument("-no-remote")
options.add_argument("-p fca-watcher")

driver = webdriver.Firefox(firefox_binary=binary, capabilities=capabilities, firefox_options=options)

driver.get('https://product.company.tld/#/login')

print(driver.title)

driver.quit()