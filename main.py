import os
import sys

import nltk
from nltk.classify import TextCat
from nltk.corpus import stopwords

from gensim.models import Word2Vec
from nltk.corpus import brown, treebank, movie_reviews

from store_load import DB
from ytscrape import getTNVideoInfo
from lang_process import TitleProcessor

WEBDRIVER_PATH = "/home/linuser/data/utils/webdrivers/geckodriver"
PROF_PATH = "/home/linuser/.mozilla/firefox/xpdj4t5a.default"
NLTK_DATA = "/home/linuser/data/utils/nltk/"
LANGS = ["eng", "deu"]


def processWriteToDB(records, db):
    """Do all the steps with records.

    1. Check for already seen links, delete seen.
    2. Filter languages. Delete records with not desired langs.
    3. Language process the titles. Do each step of TitleProcessor
    separately and write each of the results to DB.

    Args:
        records (list): List of tuples, obtained from getTNVideoInfo
    """

    i = 0
    end = len(records)
    while i < end:
        if db.isLinkInDB(records[i][0]):
            del records[i]
            end -= 1
        else:
            i += 1

    title_processor = TitleProcessor([rec[1] for rec in records], LANGS, NLTK_DATA)
    title_processor.filterDesiredLang()

    i = 0
    end = len(records)
    while i < end:
        if records[i][1] not in title_processor.selection:
            del records[i]
            end -= 1
        else:
            i += 1

    db.insertYTRawRecords(records)

    title_processor.tokenizeAlnum()
    toks_pure = [" ".join(toklist) for toklist in title_processor.processed]
    title_processor.removeStopwords()
    no_stop = [" ".join(toklist) for toklist in title_processor.processed]
    title_processor.lemmatize()
    lemmas = [" ".join(toklist) for toklist in title_processor.processed]

    db.insertProcessedRecords(
        list(zip([rec[0] for rec in records], toks_pure, no_stop, lemmas))
    )


if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("{} [path to webdriver binary] [path to firefox profile]".format(sys.argv[0]))

    # tninfo = getTNVideoInfo(WEBDRIVER_PATH, PROF_PATH)

    db = DB()

    # processWriteToDB(tninfo, db)
    processed = db.loadProcessed(
        db.yt_proc_cols["lemma"] + ", " + db.yt_proc_cols["link"]
    )
    lemmas = [s[0].split() for s in processed]
    print(processed)
    w2v = Word2Vec(lemmas, min_count=1)
    print(w2v.wv.most_similar("best"))

    # tmp update clicked videos
    db.updateClicked(("/watch?v=idfv7Lw4Y_s",))

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
