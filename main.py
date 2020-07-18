import os
import sys

import configparser

import nltk
from nltk.classify import TextCat
from nltk.corpus import stopwords

from gensim.models import Word2Vec
from nltk.corpus import brown, treebank, movie_reviews

from store_load import DB
from ytscrape import Browser, Scraper
from lang_process import TitleProcessor
from gui import GUI

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("CONFIG")
    WEBDRIVER_PATH = config["SELENIUM"]["WEBDRIVER_PATH"]
    PROF_PATH = config["SELENIUM"]["FF_PROF_PATH"]
    NLTK_DATA = config["NLTK"]["NLTK_DATA"]
    LANGS = config["PREFERENCES"]["LANGS"]

    # browser = Browser(WEBDRIVER_PATH, PROF_PATH)
    # scraper = Scraper(browser)

    db = DB()

    # processWriteToDB(tninfo, db)
    processed = db.loadProcessed(
        db.yt_proc_cols["lemma"] + ", " + db.yt_proc_cols["link"]
    )
    lemmas = [s[0].split() for s in processed]
    # print(processed)
    # w2v = Word2Vec(lemmas, min_count=1)
    # print(w2v.wv.most_similar("best"))

    # tmp update clicked videos
    # db.updateClicked(("/watch?v=idfv7Lw4Y_s",))
    # db.updateClicked(("/watch?v=LJRTINVFZDM",))
    # db.updateClicked(("/watch?v=1bzwYn8MGTs",))
    # db.updateClicked(("/watch?v=lzPgYkUBgIQ",))
    # db.updateClicked(("/watch?v=nmihGvY8NIk",))
    # db.updateClicked(("/watch?v=IQwqmutHqWA",))
    # db.updateClicked(("/watch?v=gdvMPPVQ7vY",))
    # db.updateClicked(("/watch?v=BuVj73K_ak4",))
    # db.updateClicked(("/watch?v=HjUv0Zv0T8o",))

    # print(tninfo)

    # gui = GUI(scraper, db, LANGS, NLTK_DATA)
    # gui.run()

    # el = browser.driver.find_element_by_link_text(tninfo[0][1])
    # el.click()

    # titles = [tup[1] for tup in tninfo]
    # print(tninfo)
    # print(titles)

    # title_processor = TitleProcessor(titles, LANGS, NLTK_DATA)
    # title_processor.processTitles()

    # print(title_processor.processed)
    # db = DB()
    # # for tup in tninfo:
    # select = tninfo[:]
    # for i in range(len(tninfo)):
    #     if tninfo[i][1] not in title_processor.selection:
    #         del select[i]
    # db.insertYTRawRecords(select)
    # select.append(
    #     (
    #         "/watch?v=DUMMYBLABLA",
    #         "Mdou Moctar - Tarhatazed (Live on KEXP)",
    #         "KEXP",
    #         1200000,
    #         8760,
    #         0,
    #     )
    # )
    # db.insertYTRawRecords(select)

    # rows = db.loadRaw()
    # print(rows)

    # proc = ("/watch?v=IQwqmutHqWA",) + tuple(
    #     " ".join(t) for t in [["asda", "asdsd"], ["rrrrr", "rteret"], ["sdfd", "yyyy"]]
    # )

    # db.insertProcessedRecords([proc])
