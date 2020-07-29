import os
import numpy as np

from gensim.models import FastText
from nltk.corpus import brown, treebank, movie_reviews


class FT:
    def __init__(self, db, model_fname="fasttext.model"):
        self.fname = model_fname
        self.db = db
        if not os.path.isfile(self.fname):
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

    def incTrain(self, links):
        """Do incremental training with the tokens of the scraped titles.

        Args:
            links (tuple): tuple of strings
        """
        tok_strings_scraped = self.db.loadProcessed(
            self.db.yt_proc_cols["lemma"], links=links
        )

        toks = [s[0].split() for s in tok_strings_scraped]
        self.model.build_vocab(toks, update=True)
        self.model.train(
            toks,
            total_examples=self.model.corpus_count,
            total_words=self.model.corpus_total_words,
            epochs=self.model.epochs,
        )

        self.save()

    def similScraped2Clicked(self, links):
        """Compute cosine similarity of scraped titles to all
        clicked titles.
        
        Takes links of scraped vids, loads their processed tokens,
        computes the average word vector of each title.
        Loads processed tokens of all clicked titles, computes the average
        word vector of each title and then the average of that average.

        Compute cosine similarity of the average word vectors (scraped) to
        the average of the average word vectors of all clicked titles.

        Args:
            links (tuple): tuple of strings. href links.

        Returns:
            list: list of int. cosine similarities of each scraped title.
        """
        tok_strings_scraped = self.db.loadProcessed(
            self.db.yt_proc_cols["lemma"], links=links
        )

        scraped_avg_vecs = []
        for s in tok_strings_scraped:
            tok_vecs = []
            for tok in s:
                vec = self.model.wv.word_vec(tok)
                tok_vecs.append(vec)
            scraped_avg_vecs.append(np.mean(np.array(tok_vecs), axis=0))

        tok_strings_clicked = [
            tup[0] for tup in self.db.loadClickedProc(self.db.yt_proc_cols["lemma"])
        ]

        clicked_avg_vecs = []
        for s in tok_strings_clicked:
            tok_vecs = []
            for tok in s:
                vec = self.model.wv.word_vec(tok)
                tok_vecs.append(vec)
            clicked_avg_vecs.append(np.mean(np.array(tok_vecs), axis=0))

        avg_clicked = np.mean(np.array(clicked_avg_vecs), axis=0)

        return self.model.wv.cosine_similarities(avg_clicked, scraped_avg_vecs)

    def save(self):
        self.model.save(self.fname)
