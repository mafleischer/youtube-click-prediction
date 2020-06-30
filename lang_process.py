import nltk
from nltk.classify import TextCat
from nltk.corpus import udhr


class TitleProcessor:
    def __init__(self, title_list, languages, nltk_path):
        self.title_list = title_list
        self.processed = []
        self.languages = languages
        # guesses for all titles; kind of for debug purposes
        self.lang_guesses = []
        nltk.data.path.append(nltk_path)

    def _guessLanguages(self):
        textcat = TextCat()
        for title in self.title_list:
            lang = textcat.guess_language(title)
            self.lang_guesses.append((title, lang))

    def _filterUndesiredLang(self):
        for title_lang in self.lang_guesses:
            if title_lang[1] in self.languages:
                self.processed.append(title_lang[0])

    def _cleanTitles(self, title_list):
        """Clean titles of punctuation

        Args:
            title_list (list): list of cleaned title strings
        """
        pass

    def processTitles(self):
        self._guessLanguages()
        self._filterUndesiredLang()
