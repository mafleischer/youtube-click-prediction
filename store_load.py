#!/usr/bin/python3

import sqlite3
import joblib
import os


class DB:
    def __init__(self, db_file="ytdata.sqlite3"):
        self.yttable_raw = "ytraw"
        self.yt_raw_cols = {
            "link": "href",
            "title": "title",
            "channel": "channel",
            "views": "views",
            "uploaded_time": "uploaded_hrs_ago",
            "target": "clicked",
        }

        # store all this to be able to assess multiple approaches
        # with the NLP/ML models, and to do those operations only once
        self.yttable_proc_titles = "processed_titles"
        self.yt_proc_cols = {
            "tok_pure": "token_pure",
            "no_stop": "no_stopwords",
            "lemma": "lemmatized",
        }
        if os.path.isfile(db_file):
            self.db_con = sqlite3.connect(db_file)
        else:
            print("db created")
            self.db_con = sqlite3.connect(db_file)
            self._dbInit()

    def __del__(self):
        self.db_con.commit()
        self.db_con.close()

    def _dbInit(self):
        cursor = self.db_con.cursor()
        sql_create_table_ytraw = """ CREATE TABLE IF NOT EXISTS {} (
                                        id integer PRIMARY KEY,
                                        {} text NOT NULL,
                                        {} text NOT NULL,
                                        {} text NOT NULL,
                                        {} integer NOT NULL,
                                        {} integer NOT NULL,
                                        {} integer NOT NULL);
                                """.format(
            self.yttable_raw, *self.yt_raw_cols.values()
        )
        sql_create_table_titles_proc = """ CREATE TABLE IF NOT EXISTS {} (
                                        id integer PRIMARY KEY,
                                        {} text NOT NULL,
                                        {} text NOT NULL,
                                        {} text NOT NULL);
                                """.format(
            self.yttable_proc_titles, *self.yt_proc_cols.values()
        )
        cursor.execute(sql_create_table_ytraw)
        cursor.execute(sql_create_table_titles_proc)

    def insertYTRawRecord(self, record):
        # better avoid hardcoding place of title in record?
        link_ix = list(self.yt_raw_cols.keys()).index("link")
        link = record[link_ix]
        if self.isLinkInDB(link):
            return

        sql_insert_raw = """INSERT INTO {}({}, {}, {}, {}, {}, {})
                            VALUES('{}','{}','{}',{},{},{})""".format(
            self.yttable_raw, *self.yt_raw_cols.values(), *record, 0
        )
        cursor = self.db_con.cursor()
        cursor.execute(sql_insert_raw)

    def loadRaw(self, cols="*"):
        sql_select_all_raw = """SELECT {} FROM {};""".format(cols, self.yttable_raw)
        cursor = self.db_con.cursor()
        cursor.execute(sql_select_all_raw)
        return cursor.fetchall()

    def insertProcessedRecord(self, record):
        args = [" ".join(l) for l in record]

        sql_insert_proc = """INSERT INTO {}({}, {}, {})
                            VALUES('{}','{}','{}')""".format(
            self.yttable_proc_titles, *self.yt_proc_cols.values(), *args
        )
        cursor = self.db_con.cursor()
        cursor.execute(sql_insert_proc)

    def updateRecordTarget(self, link):
        pass

    def isLinkInDB(self, link):
        sql_select_where_raw = """SELECT {0} FROM {1} WHERE {0} = '{2}';""".format(
            self.yt_raw_cols["link"], self.yttable_raw, link
        )
        cursor = self.db_con.cursor()
        cursor.execute(sql_select_where_raw)
        row = cursor.fetchall()
        if row:
            return True
        return False

