#!/usr/bin/python3

import os
import sys

import configparser

import nltk
from nltk.classify import TextCat
from nltk.corpus import stopwords

from gensim.models import Word2Vec, FastText
from nltk.corpus import brown, treebank, movie_reviews

from config import Config
from data_store_load import DB
from ytscrape import Browser, Scraper
from lang_process import TitleProcessor
from gui import GUI

if __name__ == "__main__":
    config = Config()
    config.read()
    webdriver_path = config.webdriver_path
    prof_path = config.prof_path

    db = DB()

    # browser = Browser(webdriver_path, prof_path)
    # scraper = Scraper(browser)

    # gui = GUI(browser, scraper, db)
    # gui.run()

    lemmas = [tup[0].split() for tup in db.loadProcessed("lemmatized")]
    print(lemmas)
    ft = FastText(lemmas, min_count=1)
    print(ft.wv.most_similar(["philosophy", "science", "truth"]))
    # w2v = Word2Vec(lemmas, min_count=1)
    # print(w2v.wv.most_similar(["left", "new"]))

    # db2 = DB("ytdata_new.sqlite3")
    # tninfo = [tup[1:] for tup in db.loadRaw()]
    # from db_lang_workers import Work
    # work = Work(db2)
    # work.filterRecords(tninfo)
    # work.processWriteToDB(tninfo)
