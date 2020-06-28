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


def getYTTitles(webdriver_path, firefox_profile=None):
    """Scrape the titles of the thumbnails in the youtube
    title page.

    Args:
        webdriver_path (str): path to geckodriver
        firefox_profile (str, optional): Path to firefox profile. Should be passed as it makes
        little sense for now. Defaults to None.

    Returns:
        list: List of title strings
    """

    WEBDRIVER_PATH = "/home/linuser/data/utils/webdrivers/geckodriver"
    PROF_PATH = firefox_profile
    PROF_PATH = "/home/linuser/.mozilla/firefox/xpdj4t5a.default"

    if firefox_profile:
        profile = webdriver.FirefoxProfile(profile_directory=PROF_PATH)
    else:
        profile = None

    ff_options = webdriver.FirefoxOptions()
    ff_options.add_argument("--connect-existing")
    ff_options.add_argument("--headless")

    driver = webdriver.Firefox(
        executable_path=WEBDRIVER_PATH, firefox_profile=profile, options=ff_options
    )

    driver.get("http://youtube.com/")

    src = driver.find_element_by_tag_name("html").get_attribute("outerHTML")
    driver.quit()

    f = open("yt.html", "w")
    f.write(src)
    f.close()

    soup = BeautifulSoup(src, "html.parser")
    return [tag.get("title") for tag in soup.findAll("a", {"id": "video-title-link"})]

