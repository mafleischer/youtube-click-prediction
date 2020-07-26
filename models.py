import os

from gensim.models import FastText
from nltk.corpus import brown, treebank, movie_reviews


class FT:
    def __init__(self, db, model_fname="fasttext.model"):
        self.fname = model_fname
        if not os.path.isfile(self.fname):
            self.db = db
            self.model = self._init_train()
        else:
            self.model = FastText.load(self.fname)

    def _init_train(self):
        lemmas = [tup[0].split() for tup in self.db.loadProcessed("lemmatized")]

        model = FastText(min_count=5)
        model.build_vocab(brown.sents())
        model.train(
            brown.sents(),
            total_examples=model.corpus_count,
            total_words=model.corpus_total_words,
            epochs=model.epochs,
        )
        model.build_vocab(treebank.sents(), update=True)
        model.train(
            treebank.sents(),
            total_examples=model.corpus_count,
            total_words=model.corpus_total_words,
            epochs=model.epochs,
        )
        model.build_vocab(movie_reviews.sents(), update=True)
        model.train(
            movie_reviews.sents(),
            total_examples=model.corpus_count,
            total_words=model.corpus_total_words,
            epochs=model.epochs,
        )
        model.build_vocab(lemmas, update=True)
        model.train(
            lemmas,
            total_examples=model.corpus_count,
            total_words=model.corpus_total_words,
            epochs=model.epochs,
        )

        return model

    def save(self):
        self.model.save(self.fname)
