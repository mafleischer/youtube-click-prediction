import nltk
import re
from nltk.classify import TextCat
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from HanTa import HanoverTagger

# for mapping of strings of Textcat guess to stopwords param
LANG_MAP = {"eng": "english", "deu": "german"}


class TitleProcessor:
    def __init__(self, title_list, languages, nltk_path):
        self.title_list = title_list
        self.processed = []
        self.languages = languages
        # guesses for all titles; kind of for debug purposes
        self.lang_guesses = []
        # the languages of the titles in self.processed
        self.selection_langs = []
        nltk.data.path.append(nltk_path)

    def _guessLanguages(self):
        textcat = TextCat()
        for title in self.title_list:
            lang = textcat.guess_language(title)
            self.lang_guesses.append(lang)

    def _filterDesiredLang(self):
        """Only include titles for processing of which the
        language is in self.languages.
        """
        for i in range(len(self.title_list)):
            if self.lang_guesses[i] in self.languages:
                self.processed.append(self.title_list[i])
                self.selection_langs.append(self.lang_guesses[i])

    def _filterGoodNonAlnum(self):
        """In a *single* title sort out words/terms to keep as tokens
        that have non-alphanumeric characters in them. E.g. R&B.

        Args:
            title_list (list): list of cleaned title strings
        """
        prefix = "'\"("
        infix = "&/-"
        suffix = "%'\")"
        # TODO:

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

    def _lemmatizeTokens(self, tokens, lang):
        """Lemmatize list of tokens in language lang.

        Return lemmatized as list.

        Args:
            tokens (list): list of tokens
            lang (str): language the tokens are in

        Returns:
            list: list of strings
        """
        lemmatizer = WordNetLemmatizer()
        hanta = HanoverTagger.HanoverTagger("morphmodel_ger.pgz")
        # tokenize the sentence and find the POS tag for each token
        if lang == "english":
            nltk_tagged = nltk.pos_tag(tokens)
            # tuple of (token, wordnet_tag)
            wordnet_tagged = map(
                lambda x: (x[0], self._nltkTag2WordnetTag(x[1])), nltk_tagged
            )
            lemmatized = []
            for word, tag in wordnet_tagged:
                if tag is None:
                    # if there is no available tag, append the token as is
                    lemmatized.append(word)
                else:
                    # else use the tag to lemmatize the token
                    lemmatized.append(lemmatizer.lemmatize(word, tag))

        if lang == "german":
            tups_taglemmapos = hanta.tag_sent(tokens)
            lemmatized = [tup[1] for tup in tups_taglemmapos]

        return lemmatized

    def _tokenizeFilterLemma(self):
        """Tokenize, filter non-alnum strings, call
        lemmatizing function, make lower case

        TODO: call the other filter function which will
        filter on other criteria: keep words like R&B as a
        token.
        """
        for i in range(len(self.processed)):
            toks = word_tokenize(self.processed[i])
            filtered_toks = []
            for t in range(len(toks)):
                if toks[t].isalnum():
                    lang = LANG_MAP[self.selection_langs[i]]
                    if toks[t] not in stopwords.words(lang):
                        filtered_toks.append(toks[t])
            lemmatized = [
                tok.lower() for tok in self._lemmatizeTokens(filtered_toks, lang)
            ]
            self.processed[i] = lemmatized

    def processTitles(self):
        self._guessLanguages()
        self._filterDesiredLang()
        self._tokenizeFilterLemma()
