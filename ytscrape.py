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


class Browser:
    def __init__(self, webdriver_path, firefox_profile=None):
        if firefox_profile:
            self.profile = webdriver.FirefoxProfile(profile_directory=firefox_profile)
        else:
            self.profile = None

        ff_options = webdriver.FirefoxOptions()
        ff_options.add_argument("--connect-existing")
        # ff_options.add_argument(

        self.driver = webdriver.Firefox(
            executable_path=webdriver_path,
            firefox_profile=firefox_profile,
            options=ff_options,
        )

    def __del__(self):
        self.driver.quit()


class Scraper:
    def __init__(self, browser):
        self.browser = browser

    def getYouTube(self):
        self.browser.driver.get("http://youtube.com/")

    def getTNVideoInfo(self):
        """Scrape the titles of the thumbnails in the youtube
        home page (signed out).

        Args:
            webdriver_path (str): path to geckodriver
            firefox_profile (str, optional): Path to firefox profile. Should be passed as it makes
            little sense for now. Defaults to None.

        Returns:
            list: List of tuples: (link, title string)
        """

        self.getYouTube()
        src = self.browser.driver.find_element_by_tag_name("html").get_attribute(
            "outerHTML"
        )

        # f = open("yt.html", "w")
        # f.write(src)
        # f.close()

        # stub for now
        # f = open("yt.html", "r")
        # src = f.read()
        # f.close()

        soup = BeautifulSoup(src, "html.parser")

        # Get rid of "COVID-19 news" section
        for descendant in soup.select(
            "ytd-rich-section-renderer.style-scope:nth-child(14) > div:nth-child(1)"
        ):
            descendant.decompose()

        f = open("yt2.html", "w")
        f.write(str(soup))
        f.close()

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

        # process number strings in views

        pat_num = re.compile("[0-9]*(?:\.[0-9]*)?")
        pat_k = re.compile("K")
        pat_m = re.compile("M")
        for i in range(len(views)):
            vstr = views[i]
            num = float(pat_num.match(vstr).group())
            k = pat_k.search(vstr)
            m = pat_m.search(vstr)
            if k:
                num *= 1000
            elif m:
                num *= 1000000
            views[i] = int(num)

        # convert uploaded time strings to number of hours

        pat_num = re.compile("[0-9]*")
        pat_min = re.compile("minutes")
        pat_hrs = re.compile("hour[s]?")
        pat_d = re.compile("day[s]?")
        pat_we = re.compile("week[s]?")
        pat_mon = re.compile("month[s]?")
        pat_yrs = re.compile("year[s]?")

        for i in range(len(uploaded_time)):
            tstr = uploaded_time[i]
            num = int(pat_num.match(tstr).group())
            mins = pat_min.search(tstr)
            hrs = pat_hrs.search(tstr)
            d = pat_d.search(tstr)
            we = pat_we.search(tstr)
            mon = pat_mon.search(tstr)
            yrs = pat_yrs.search(tstr)
            if mins:
                num = 0
            elif hrs:
                pass
            elif d:
                num *= 24
            elif we:
                num *= 24 * 7
            elif mon:
                num *= 24 * 31
            elif yrs:
                num *= 24 * 365
            uploaded_time[i] = num

        all_targets_0 = [0] * len(link)
        return list(zip(link, title, channel, views, uploaded_time, all_targets_0))
