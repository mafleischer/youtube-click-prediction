from tkinter import Tk, Frame, Button, Listbox
from tkinter import RIGHT, LEFT, TOP, BOTTOM, END
from tkinter import SINGLE

# tmp
import numpy as np

from db_lang_workers import Work
from models import FT


def fn():
    # dummy
    pass


class GUI:
    def __init__(self, browser, scraper, db):
        self.browser = browser
        self.scraper = scraper
        self.db = db
        self.ft = FT(self.db)
        self.records = []  # used subsequently for listbox

        self.root = Tk()
        self.root.title("YouTube - Predict next click")

        self.frame_right = Frame(self.root, borderwidth=10, height=360, width=200)
        self.frame_right.pack(side=RIGHT)
        self.frame_right.pack_propagate(0)
        self.frame_left = Frame(self.root, borderwidth=10, height=360, width=350)
        self.frame_left.pack(side=LEFT)
        self.frame_left.pack_propagate(0)

        self.button_scrape = Button(
            self.frame_right, text="Scrape YT", width=50, command=self.clickYTScrape
        )
        self.button_scrape.pack(side=TOP)

        self.button_click = Button(
            self.frame_right,
            text="Click selection",
            width=50,
            command=self.clickClickSelection,
        )
        self.button_click.pack(side=TOP)

        self.button_visuals = Button(
            self.frame_right, text="Visuals", width=50, command=fn
        )
        self.button_visuals.pack(side=TOP, pady=20)

        self.button_quit = Button(
            self.frame_right, text="Quit", width=50, command=self.__del__
        )
        self.button_quit.pack(side=TOP)

        self.listbox = Listbox(
            self.frame_left, selectmode=SINGLE, height=350, width=200
        )
        self.listbox.pack(side=BOTTOM)
        self.listbox.bind("<Double-Button-1>", fn)

    def __del__(self):
        del self.scraper
        del self.db
        self.root.destroy()

    def run(self):
        self.root.mainloop()

    def clickYTScrape(self):
        """Scrape, filter, process/insert,
        fill the listbox with the title strings.
        """
        self.listbox.delete(0, END)
        tninfo = self.scraper.getTNVideoInfo()
        work = Work(self.db)
        work.filterRecords(tninfo)
        work.processWriteToDB(tninfo)
        self.records = tninfo
        self.listbox.delete(0, END)
        links = []
        for rec in tninfo:
            links.append(rec[0])
            title = rec[1]

            print(title)

            self.listbox.insert(END, title)

        # train model and compute click likelihood for scraped videos

        tok_strings_scraped = self.db.loadProcessed(
            self.db.yt_proc_cols["lemma"], links=tuple(links)
        )

        toks = [s[0].split() for s in tok_strings_scraped]
        self.ft.model.build_vocab(toks, update=True)
        self.ft.model.train(
            toks,
            total_examples=self.ft.model.corpus_count,
            total_words=self.ft.model.corpus_total_words,
            epochs=self.ft.model.epochs,
        )

        self.ft.save()

        scraped_avg_vecs = []
        for s in tok_strings_scraped:
            tok_vecs = []
            for tok in s:
                vec = self.ft.model.wv.word_vec(tok)
                tok_vecs.append(vec)
            scraped_avg_vecs.append(np.mean(np.array(tok_vecs), axis=0))

        tok_strings_clicked = [
            tup[0] for tup in self.db.loadClickedProc(self.db.yt_proc_cols["lemma"])
        ]
        clicked_avg_vecs = []
        for s in tok_strings_clicked:
            tok_vecs = []
            for tok in s:
                vec = self.ft.model.wv.word_vec(tok)
                tok_vecs.append(vec)
            clicked_avg_vecs.append(np.mean(np.array(tok_vecs), axis=0))

        avg_clicked = np.mean(np.array(clicked_avg_vecs), axis=0)

        # avg_scraped = np.mean(np.array(scraped_avg_vecs), axis=0)
        # print(self.ft.model.wv.cosine_similarities(avg_clicked, [avg_scraped]))
        similarities = list(
            zip(
                self.ft.model.wv.cosine_similarities(avg_clicked, scraped_avg_vecs),
                tok_strings_scraped,
            )
        )
        print(similarities)

    def clickClickSelection(self):
        sel = self.listbox.curselection()
        if sel:
            link = self.records[sel[0]][0]
            self.browser.clickLink(link)
            self.db.updateClicked(link)
