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

    browser = Browser(webdriver_path, prof_path)
    scraper = Scraper(browser)

    gui = GUI(browser, scraper, db)
    gui.run()

    # lemmas = [tup[0].split() for tup in db.loadProcessed("lemmatized")]

    # ft = FT(db)
    # ft.save()

    # vecs1 = np.array(
    #     [
    #         ft.model.wv.word_vec("philosopy"),
    #         ft.model.wv.word_vec("science"),
    #         ft.model.wv.word_vec("brain"),
    #         ft.model.wv.word_vec("talk"),
    #     ]
    # )
    # vecs2 = np.array(
    #     [
    #         ft.model.wv.word_vec("joe"),
    #         ft.model.wv.word_vec("rogan"),
    #         ft.model.wv.word_vec("science"),
    #         ft.model.wv.word_vec("math"),
    #     ]
    # )
    # vecs3 = np.array(
    #     [
    #         ft.model.wv.word_vec("read"),
    #         ft.model.wv.word_vec("men"),
    #         ft.model.wv.word_vec("science"),
    #         ft.model.wv.word_vec("peterson"),
    #     ]
    # )

    # avg1 = np.mean(vecs1, axis=0)
    # avg2 = np.mean(vecs2, axis=0)
    # avg3 = np.mean(vecs3, axis=0)

    # strs = [tup[0] for tup in db.loadClickedProc(db.yt_proc_cols["lemma"])]
    # clicked_vecs = []
    # for s in strs:
    #     title_vecs = []
    #     for word in s:
    #         vec = ft.model.wv.word_vec(word)
    #         title_vecs.append(vec)
    #     clicked_vecs.append(np.mean(np.array(title_vecs), axis=0))

    # avg_clicked = np.mean(np.array(clicked_vecs), axis=0)
    # print(ft.model.wv.cosine_similarities(avg_clicked, [avg1, avg2, avg3]))

    # db2 = DB("ytdata_new.sqlite3")
    # tninfo = [tup[1:] for tup in db.loadRaw()]
    # from db_lang_workers import processWriteToDB

    # title_processor = TitleProcessor([tup[1] for tup in tninfo[815:]])
    # title_processor.guessLanguages()
    # title_processor.selection_langs = title_processor.lang_guesses
    # processWriteToDB(tninfo[815:], db2, title_processor)
