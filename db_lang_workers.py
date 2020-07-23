from lang_process import TitleProcessor


class Work:
    def __init__(self, db):
        self.db = db
        self.title_processor = None

    def filterRecords(self, records):
        """Delete record tuples from list that are not in
        languages pref. or are already in the DB.
        
        The latter only saves the superfluous work of processing
        titles again.

        Args:
            records (list): list of tuples, records of raw data
        """

        i = 0
        end = len(records)
        while i < end:
            if self.db.isLinkInDB(records[i][0]):
                del records[i]
                end -= 1
            else:
                i += 1

        self.title_processor = TitleProcessor([rec[1] for rec in records])
        self.title_processor.filterDesiredLang()

        i = 0
        end = len(records)
        while i < end:
            if records[i][1] not in self.title_processor.selection:
                del records[i]
                end -= 1
            else:
                i += 1

    def processWriteToDB(self, records):
        """Insert records, do the processing steps.

        Language process the titles. Do each step of TitleProcessor
        separately and write each of the results to DB.

        Args:
            records (list): List of tuples, obtained from getTNVideoInfo
            db (DB): DB object
        """

        self.db.insertYTRawRecords(records)

        # title_processor = TitleProcessor([rec[1] for rec in records])
        self.title_processor.tokenizeAlnum()
        toks_pure = [" ".join(toklist) for toklist in self.title_processor.processed]
        self.title_processor.removeStopwords()
        no_stop = [" ".join(toklist) for toklist in self.title_processor.processed]
        self.title_processor.lemmatize()
        lemmas = [" ".join(toklist) for toklist in self.title_processor.processed]

        self.db.insertProcessedRecords(
            list(zip([rec[0] for rec in records], toks_pure, no_stop, lemmas))
        )
