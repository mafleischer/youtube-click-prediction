import configparser


class Config:
    def __init__(self, file="CONFIG"):
        self.file = file

    def read(self):
        config = configparser.ConfigParser()
        config.read(self.file)
        self.webdriver_path = config["SELENIUM"]["WEBDRIVER_PATH"]
        self.prof_path = config["SELENIUM"]["FF_PROF_PATH"]
        self.nltk_data = config["NLTK"]["NLTK_DATA"]
        self.langs = config["PREFERENCES"]["LANGS"].split()
