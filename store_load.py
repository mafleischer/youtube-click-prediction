#!/usr/bin/python3

import sqlite3
import joblib


class DB:
    def __init__(self, db_file="ytdata.sqlite3"):
        self.db_con = sqlite3.connect(db_file)
        self.yt_col_names = {
            "link": "href",
            "title": "title",
            "channel": "channel",
            "views": "views",
            "uploaded_time": "uploaded_hrs_ago",
            "target": "clicked",
        }

    def insertYTRecord(record):
        pass

    def loadAll():
        pass

    def updateRecordTarget(title):
        pass

    def isTitleInDB(title):
        pass

