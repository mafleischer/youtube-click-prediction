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
            "link": self.yt_raw_cols["link"],
            "tok_pure": "token_pure",
            "no_stop": "no_stopwords",
            "lemma": "lemmatized",
        }
        if os.path.isfile(db_file):
            self.db_con = sqlite3.connect(db_file)
        else:
            print("DB file created")
            self.db_con = sqlite3.connect(db_file)
            self._dbInit()

    def __del__(self):
        self.db_con.commit()
        self.db_con.close()

    def _dbInit(self):
        sql_create_table_ytraw = """ CREATE TABLE IF NOT EXISTS {} (
                                        id INTEGER PRIMARY KEY,
                                        {} TEXT NOT NULL UNIQUE,
                                        {} TEXT NOT NULL,
                                        {} TEXT NOT NULL,
                                        {} INTEGER NOT NULL,
                                        {} INTEGER NOT NULL,
                                        {} INTEGER NOT NULL);
                                """.format(
            self.yttable_raw, *self.yt_raw_cols.values()
        )

        sql_pragma_foreign = "PRAGMA foreign_keys = ON;"

        sql_create_table_titles_proc = """CREATE TABLE IF NOT EXISTS {0} (
                                        id INTEGER PRIMARY KEY,
                                        {1} TEXT NOT NULL UNIQUE,
                                        {2} TEXT NOT NULL,
                                        {3} TEXT NOT NULL,
                                        {4} TEXT NOT NULL,
                                        FOREIGN KEY({1}) REFERENCES {5}({1}));
                                """.format(
            self.yttable_proc_titles, *self.yt_proc_cols.values(), self.yttable_raw,
        )
        self.db_con.execute(sql_create_table_ytraw)
        self.db_con.execute(sql_pragma_foreign)
        self.db_con.execute(sql_create_table_titles_proc)

    def insertYTRawRecords(self, records):
        sql_insert_raw = """INSERT OR IGNORE INTO {}({}, {}, {}, {}, {}, {})
                            VALUES(?,?,?,?,?,?)""".format(
            self.yttable_raw, *self.yt_raw_cols.values()
        )
        self.db_con.executemany(sql_insert_raw, records)

    def insertProcessedRecords(self, records):
        sql_insert_proc = """INSERT OR IGNORE INTO {}({}, {}, {}, {})
                            VALUES(?,?,?,?)""".format(
            self.yttable_proc_titles, *self.yt_proc_cols.values(),
        )
        self.db_con.executemany(sql_insert_proc, records)

    def loadRaw(self, cols="*"):
        sql_select_all_raw = """SELECT {} FROM {};""".format(cols, self.yttable_raw)
        cursor = self.db_con.execute(sql_select_all_raw)
        return cursor.fetchall()

    def loadProcessed(self, cols="*"):
        sql_select_all_raw = """SELECT {} FROM {};""".format(
            cols, self.yttable_proc_titles
        )
        cursor = self.db_con.execute(sql_select_all_raw)
        return cursor.fetchall()

    def loadClicked(self, cols="*"):
        sql_select_clicked_raw = """SELECT {} FROM {} WHERE {} = 1;""".format(
            cols, self.yttable_raw, self.yt_raw_cols["target"]
        )
        cursor = self.db_con.execute(sql_select_clicked_raw)
        return cursor.fetchall()

    def loadClickedProc(self, cols="*"):
        clicked_links = tuple(
            tup[0] for tup in self.loadClicked(self.yt_raw_cols["link"])
        )

        param_str = "?, " * (len(clicked_links) - 1) + "?"

        sql_select_clicked_proc = """SELECT {} FROM {} WHERE {} in ({});""".format(
            cols, self.yttable_proc_titles, self.yt_proc_cols["link"], param_str
        )
        cursor = self.db_con.execute(sql_select_clicked_proc, clicked_links)
        return cursor.fetchall()

    def updateClicked(self, link):
        sql_update = """UPDATE {} SET {} = 1 WHERE {} = ?;""".format(
            self.yttable_raw, self.yt_raw_cols["target"], self.yt_raw_cols["link"]
        )
        self.db_con.execute(sql_update, (link,))

    def isLinkInDB(self, link):
        sql_select_where_raw = """SELECT {0} FROM {1} WHERE {0} = '{2}';""".format(
            self.yt_raw_cols["link"], self.yttable_raw, link
        )
        cursor = self.db_con.execute(sql_select_where_raw)
        row = cursor.fetchall()
        if row:
            return True
        return False

