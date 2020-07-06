import os
import sys

import nltk
from nltk.classify import TextCat
from nltk.corpus import stopwords

from ytscrape import getYTTitles
from lang_process import TitleProcessor

WEBDRIVER_PATH = "/home/linuser/data/utils/webdrivers/geckodriver"
PROF_PATH = "/home/linuser/.mozilla/firefox/xpdj4t5a.default"
NLTK_PATH = "/home/linuser/data/utils/nltk/"
LANGS = ["eng", "deu"]

if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("{} [path to webdriver binary] [path to firefox profile]".format(sys.argv[0]))
    titles = getYTTitles(WEBDRIVER_PATH, PROF_PATH)
    print(titles)

    title_processor = TitleProcessor(titles, LANGS, NLTK_PATH)
    title_processor.processTitles()

    print(title_processor.processed)
