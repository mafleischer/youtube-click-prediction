import nltk
import re
from nltk.classify import TextCat
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from HanTa import HanoverTagger
from gensim.models import Word2Vec

# for mapping of strings of Textcat guess to stopwords param
LANG_MAP = {"eng": "english", "deu": "german"}


class TitleProcessor:
    def __init__(self, title_list, languages, nltk_data):
        self.title_list = title_list
        self.processed = []
        self.languages = languages
        # guesses for all titles; kind of for debug purposes
        self.lang_guesses = []
        self.selection = []
        self.selection_langs = []
        nltk.data.path.append(nltk_data)
        self.lemmatizers = {
            "english": WordNetLemmatizer(),
            "german": HanoverTagger.HanoverTagger("morphmodel_ger.pgz"),
        }

    def _guessLanguages(self):
        textcat = TextCat()
        for title in self.title_list:
            lang = textcat.guess_language(title)
            # strangely guess_language puts a space at the end sometimes
            lang = lang.rstrip()
            self.lang_guesses.append(lang)

    def filterDesiredLang(self):
        """Only include titles for processing of which the
        language is in self.languages, created by _guessLanguages().
        """
        self._guessLanguages()

        for i in range(len(self.title_list)):
            if self.lang_guesses[i] in self.languages:
                self.selection.append(self.title_list[i])
                self.selection_langs.append(self.lang_guesses[i])
                self.processed.append(self.title_list[i])

    def tokenizeAlnum(self):
        for i in range(len(self.processed)):
            toks = word_tokenize(self.processed[i])
            filtered_toks = []
            for t in range(len(toks)):
                if toks[t].isalnum():
                    filtered_toks.append(toks[t])
            self.processed[i] = filtered_toks

    def tokenizeExceptions(self):
        """In a *single* title sort out words/terms to keep as tokens
        that have non-alphanumeric characters in them. E.g. R&B.

        Args:
            title_list (list): list of cleaned title strings
        """
        prefix = "'\"("
        infix = "&/-"
        suffix = "%'\")"
        # TODO:

    def removeStopwords(self):
        for i in range(len(self.processed)):
            toks = self.processed[i]
            filtered_toks = []
            lang = LANG_MAP[self.selection_langs[i]]
            for t in range(len(toks)):
                if toks[t].lower() not in stopwords.words(lang):
                    filtered_toks.append(toks[t])
            self.processed[i] = filtered_toks

    def _nltkTag2WordnetTag(self, nltk_tag):
        """Return corresponding wordnet POS tag
        to nltk.pos_tag tag.

        Args:
            nltk_tag (str): tag in tuple obtained by pos_tag call

        Returns:
            str: wordnet tag
        """
        if nltk_tag.startswith("J"):
            return wordnet.ADJ
        elif nltk_tag.startswith("V"):
            return wordnet.VERB
        elif nltk_tag.startswith("N"):
            return wordnet.NOUN
        elif nltk_tag.startswith("R"):
            return wordnet.ADV
        else:
            return None

    def lemmatize(self):
        """Lemmatize all lists of tokens in self.processed.
        """

        # tokenize the sentence and find the POS tag for each token
        for i in range(len(self.processed)):
            lang = LANG_MAP[self.selection_langs[i]]
            lemmatized = []
            if lang == "english":
                wordnet = self.lemmatizers[lang]
                nltk_tagged = nltk.pos_tag(self.processed[i])
                # tuple of (token, wordnet_tag)
                wordnet_tagged = map(
                    lambda x: (x[0], self._nltkTag2WordnetTag(x[1])), nltk_tagged
                )
                for word, tag in wordnet_tagged:
                    if tag is None:
                        # if there is no available tag, append the token as is
                        lemmatized.append(word.lower())
                    else:
                        # else use the tag to lemmatize the token
                        lemmatized.append(wordnet.lemmatize(word, tag).lower())

            if lang == "german":
                hanta = self.lemmatizers[lang]
                tups_taglemmapos = hanta.tag_sent(self.processed[i])
                lemmatized = [tup[1].lower() for tup in tups_taglemmapos]

            self.processed[i] = lemmatized

    def processTitles(self):
        self.filterDesiredLang()
        self.tokenizeAlnum()
        self.removeStopwords()
        self.lemmatize()
