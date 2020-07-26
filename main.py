#!/usr/bin/python3

import os
import sys

import numpy as np

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
from models import FT
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
    # print(lemmas)

    ft = FT(db)
    # ft.save()

    vecs1 = np.array(
        [
            ft.model.wv.word_vec("philosopy"),
            ft.model.wv.word_vec("science"),
            ft.model.wv.word_vec("brain"),
            ft.model.wv.word_vec("talk"),
        ]
    )
    # vecs2 = np.array(
    #     [
    #         ft.model.wv.word_vec("jordan"),
    #         ft.model.wv.word_vec("peterson"),
    #         ft.model.wv.word_vec("truth"),
    #         ft.model.wv.word_vec("joe"),
    #     ]
    # )
    # vecs2 = np.array(
    #     [
    #         ft.model.wv.word_vec("philosopy"),
    #         ft.model.wv.word_vec("science"),
    #         ft.model.wv.word_vec("brain"),
    #         ft.model.wv.word_vec("math"),
    #     ]
    # )
    vecs2 = np.array(
        [
            ft.model.wv.word_vec("trash"),
            ft.model.wv.word_vec("happy"),
            ft.model.wv.word_vec("sword"),
            ft.model.wv.word_vec("fighting"),
        ]
    )

    avg1 = np.mean(vecs1, axis=0)
    avg2 = np.mean(vecs2, axis=0)
    print(ft.model.wv.cosine_similarities(avg1, [avg2]))
    print(ft.model.wv.wmdistance(["science", "brain"], ["science", "brainwaves"]))

    # w2v = Word2Vec(lemmas, min_count=1)
    # print(w2v.wv.wmdistance(["left", "new"]))

    # db2 = DB("ytdata_new.sqlite3")
    # tninfo = [tup[1:] for tup in db.loadRaw()]
    # from db_lang_workers import Work
    # work = Work(db2)
    # work.filterRecords(tninfo)
    # work.processWriteToDB(tninfo)
