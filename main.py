import os
import sys

import nltk
from nltk.classify import TextCat
from nltk.corpus import stopwords

from store_load import DB
from ytscrape import getTNVideoInfo
from lang_process import TitleProcessor

WEBDRIVER_PATH = "/home/linuser/data/utils/webdrivers/geckodriver"
PROF_PATH = "/home/linuser/.mozilla/firefox/xpdj4t5a.default"
NLTK_DATA = "/home/linuser/data/utils/nltk/"
LANGS = ["eng", "deu"]

if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("{} [path to webdriver binary] [path to firefox profile]".format(sys.argv[0]))
    tninfo = getTNVideoInfo(WEBDRIVER_PATH, PROF_PATH)
    titles = [tup[1] for tup in tninfo]
    print(tninfo)
    print(titles)

    title_processor = TitleProcessor(titles, LANGS, NLTK_DATA)
    title_processor.processTitles()

    print(title_processor.processed)
    db = DB()
    for tup in tninfo:
        args = list(tup)
        db.insertYTRawRecord(args)

    rows = db.loadRaw()
    print(rows)
