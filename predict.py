import os
import sys

from ytscrape import getYTTitles

WEBDRIVER_PATH = "/home/linuser/data/utils/webdrivers/geckodriver"
PROF_PATH = "/home/linuser/.mozilla/firefox/xpdj4t5a.default"

if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("{} [path to webdriver binary] [path to firefox profile]".format(sys.argv[0]))
    titles = getYTTitles(WEBDRIVER_PATH, PROF_PATH)
    print(titles)
