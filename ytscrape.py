#!/usr/bin/python3

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

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
ff_options.add_argument("--connect-existing")
ff_options.add_argument("--headless")


driver = webdriver.Firefox(
    executable_path=WEBDRIVER_PATH, firefox_profile=profile, options=ff_options
)

wait = WebDriverWait(driver, 10)
driver.get("http://youtube.com/")
# wait.until(ec.presence_of_all_elements_located((By.ID, "video-title-link")))

src = driver.find_element_by_tag_name("html").get_attribute("outerHTML")
# page = driver.page_source
f = open("yt.html", "w")
f.write(src)
f.close()

# elements = driver.find_element_by_id("video-title-link")
# print(elements.get_attribute("title"))

soup = BeautifulSoup(src, "html.parser")
for tag in soup.findAll("a", {"id": "video-title-link"}):
    print(tag.get("title"))

driver.quit()

