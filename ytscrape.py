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
import re
import sqlite3

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


def getTNVideoInfo(webdriver_path, firefox_profile=None):
    """Scrape the titles of the thumbnails in the youtube
    home page (signed out).

    Args:
        webdriver_path (str): path to geckodriver
        firefox_profile (str, optional): Path to firefox profile. Should be passed as it makes
        little sense for now. Defaults to None.

    Returns:
        list: List of tuples: (link, title string)
    """

    WEBDRIVER_PATH = "/home/linuser/data/utils/webdrivers/geckodriver"
    PROF_PATH = firefox_profile
    PROF_PATH = "/home/linuser/.mozilla/firefox/xpdj4t5a.default"

    # if firefox_profile:
    #     profile = webdriver.FirefoxProfile(profile_directory=PROF_PATH)
    # else:
    #     profile = None

    # ff_options = webdriver.FirefoxOptions()
    # ff_options.add_argument("--connect-existing")
    # ff_options.add_argument("--headless")

    # driver = webdriver.Firefox(
    #     executable_path=WEBDRIVER_PATH, firefox_profile=profile, options=ff_options
    # )

    # driver.get("http://youtube.com/")

    # src = driver.find_element_by_tag_name("html").get_attribute("outerHTML")
    # driver.quit()

    # f = open("yt.html", "w")
    # f.write(src)
    # f.close()

    # stub for now
    f = open("yt.html", "r")
    src = f.read()
    f.close()

    soup = BeautifulSoup(src, "html.parser")

    # Get rid of "COVID-19 news" section
    for descendant in soup.select(
        "ytd-rich-section-renderer.style-scope:nth-child(14) > div:nth-child(1)"
    ):
        descendant.decompose()

    f = open("yt2.html", "w")
    f.write(str(soup))
    f.close()

    # details = soup.findAll("a", {"id" : "avatar-link"})

    # info = []
    # for detail in details:
    #     channel = detail.get("title")
    #     channel_link = detail.get("href")
    #     link_tag = detail.findChildren("a", {"id": "video-title-link"}

    a_title = soup.findAll("a", {"id": "video-title-link"})

    link = [tag.get("href") for tag in a_title]
    title = [tag.get("title") for tag in a_title]

    a_channel = soup.select(
        "ytd-rich-item-renderer.ytd-rich-grid-renderer > div > ytd-rich-grid-video-renderer > div > div > div > ytd-video-meta-block > div > div > ytd-channel-name > div > div > yt-formatted-string > a:nth-child(1)"
    )
    channel = [a.text for a in a_channel]

    spans_views = soup.select(
        "ytd-rich-item-renderer.ytd-rich-grid-renderer > div > ytd-rich-grid-video-renderer > div > div > div > ytd-video-meta-block > div > div > span:nth-child(1)"
    )
    views = [span.text for span in spans_views]

    spans_uploaded_time = soup.select(
        "ytd-rich-item-renderer.ytd-rich-grid-renderer > div > ytd-rich-grid-video-renderer > div > div > div > ytd-video-meta-block > div > div > span:nth-child(2)"
    )
    uploaded_time = [span.text for span in spans_uploaded_time]

    return list(zip(link, title, channel, views, uploaded_time))

    # return [
    #     (vid_details.get("href"), vid_details.get("title"), details.)
    #     for tag in soup.findAll("a", {"id": "video-title-link"})
    # ]

