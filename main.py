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
    # ft = FastText(lemmas, min_count=1)
    # # print(
    # #     ft.wv.cosine_similarities(
    # #         ["philosophy", "science", "truth"], ["brain", "study", "talk"]
    # #     )
    # # )
    # vecs1 = np.array(
    #     [
    #         ft.wv.word_vec("philosopy"),
    #         ft.wv.word_vec("science"),
    #         ft.wv.word_vec("brain"),
    #         ft.wv.word_vec("talk"),
    #     ]
    # )
    # vecs2 = np.array(
    #     [
    #         ft.wv.word_vec("joe"),
    #         ft.wv.word_vec("rogan"),
    #         ft.wv.word_vec("science"),
    #         ft.wv.word_vec("talk"),
    #     ]
    # )
    # avg1 = np.mean(vecs1, axis=0)
    # avg2 = np.mean(vecs2, axis=0)
    # print(ft.wv.cosine_similarities(avg1, [avg2]))

    ft = FastText(min_count=1)
    ft = FastText.load("ft_tmp.model")

    ft.build_vocab(brown.sents())
    ft.train(
        brown.sents(),
        total_examples=ft.corpus_count,
        total_words=ft.corpus_total_words,
        epochs=ft.epochs,
    )
    # ft.build_vocab(movie_reviews.sents(), update=True)
    # ft.train(
    #     movie_reviews.sents(),
    #     total_examples=ft.corpus_count,
    #     total_words=ft.corpus_total_words,
    #     epochs=ft.epochs,
    # )
    # ft.build_vocab(lemmas, update=True)
    # ft.train(
    #     lemmas,
    #     total_examples=ft.corpus_count,
    #     total_words=ft.corpus_total_words,
    #     epochs=ft.epochs,
    # )

    # ft.save("ft_tmp.model")

    vecs1 = np.array(
        [
            ft.wv.word_vec("philosopy"),
            ft.wv.word_vec("science"),
            ft.wv.word_vec("brain"),
            ft.wv.word_vec("talk"),
        ]
    )
    vecs2 = np.array(
        [
            ft.wv.word_vec("feces"),
            ft.wv.word_vec("cab"),
            ft.wv.word_vec("cabbage"),
            ft.wv.word_vec("devil"),
        ]
    )

    avg1 = np.mean(vecs1, axis=0)
    avg2 = np.mean(vecs2, axis=0)
    print(ft.wv.cosine_similarities(avg1, [avg2]))

    # w2v = Word2Vec(lemmas, min_count=1)
    # print(w2v.wv.wmdistance(["left", "new"]))

    # db2 = DB("ytdata_new.sqlite3")
    # tninfo = [tup[1:] for tup in db.loadRaw()]
    # from db_lang_workers import Work
    # work = Work(db2)
    # work.filterRecords(tninfo)
    # work.processWriteToDB(tninfo)
