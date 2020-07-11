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
        if os.path.isfile(db_file):
            self.db_con = sqlite3.connect(db_file)
        else:
            print("db created")
            self.db_con = sqlite3.connect(db_file)
            self._dbInit()

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
        cursor.execute(sql_create_table_ytraw)

    def insertYTRawRecord(self, record):
        # better avoid hardcoding place of title in record?
        title_ix = list(self.yt_raw_cols.keys()).index("title")
        title = record[title_ix]
        if self.isTitleInDB(title):
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

    def updateRecordTarget(self, title):
        pass

    def isTitleInDB(self, title):
        sql_select_where_raw = """SELECT {0} FROM {1} WHERE {0} = '{2}';""".format(
            self.yt_raw_cols["title"], self.yttable_raw, title
        )
        cursor = self.db_con.cursor()
        cursor.execute(sql_select_where_raw)
        row = cursor.fetchall()
        if row:
            return True
        return False

