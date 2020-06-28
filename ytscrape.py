#!/usr/bin/python3

from bs4 import BeautifulSoup
from selenium import webdriver

import time
import urllib3
import requests
import os

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


WEBDRIVER_PATH = "/home/linuser/data/utils/webdrivers/geckodriver"
PROF_PATH = "/home/linuser/.mozilla/firefox/xpdj4t5a.default"
capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()

profile = webdriver.FirefoxProfile(profile_directory=PROF_PATH)
# profile.set_preference("browser.cache.disk.enable", True)
# profile.set_preference("browser.cache.memory.enable", True)
# profile.set_preference("browser.cache.offline.enable", True)
# profile.set_preference("network.http.use-cache", True)

ff_options = webdriver.FirefoxOptions()
# ff_options.add_argument("--connect-existing")
# ff_options.add_argument("--headless")


driver = webdriver.Firefox(
    executable_path=WEBDRIVER_PATH, firefox_profile=profile, options=ff_options
)
driver.get("http://youtube.com/")
time.sleep(5)  # Let the user actually see something!
# driver.quit()

# page = requests.get("http://youtube.com/")
# f = open("yt.html", "w")
# f.write(page.text)
# f.close()
