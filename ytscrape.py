#!/usr/bin/python3

from bs4 import BeautifulSoup
from selenium import webdriver

import time
import urllib3

# problem with chromium, error message
# WEBDRIVER_PATH = "/home/linuser/data/utils/webdrivers/chromedriver"

# capabilities = {
#     "browserName": "chrome",
#     "chromeOptions": {
#         "useAutomationExtension": False,
#         "forceDevToolsScreenshot": True,
#         "args": ["--start-maximized", "--disable-infobars"],
#     },
# }

# capabilities = webdriver.DesiredCapabilities.CHROME.copy()
# capabilities["useAutomationExtension"] = False

# chrome_options = webdriver.ChromeOptions()
# # chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--start-maximized")

# driver = webdriver.Chrome(
#     WEBDRIVER_PATH, desired_capabilities=capabilities, options=chrome_options
# )


WEBDRIVER_PATH = "/home/linuser/data/utils/webdrivers/"
capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
driver = webdriver.Firefox(WEBDRIVER_PATH)
driver.get("http://www.google.com/")
search_box = driver.find_element_by_name("q")
search_box.send_keys("FirefoxDriver")
search_box.submit()
time.sleep(5)  # Let the user actually see something!
driver.quit()
