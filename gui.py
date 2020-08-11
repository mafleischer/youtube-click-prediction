from tkinter import Tk, Frame, Button, Listbox
from tkinter import RIGHT, LEFT, TOP, BOTTOM, END
from tkinter import SINGLE

# tmp
import numpy as np

from db_lang_workers import Work
from models import FT


class GUI:
    def __init__(self, browser, scraper, db):
        self.browser = browser
        self.scraper = scraper
        self.db = db
        self.ft = FT(self.db)
        self.records = []  # used subsequently for listbox
        self.click_prob = []  # holds probabilites / similarities of scraped titles

        self.root = Tk()
        self.root.title("YouTube - Predict next click")

        self.frame_right = Frame(self.root, borderwidth=10, height=360, width=200)
        self.frame_right.pack(side=RIGHT)
        self.frame_right.pack_propagate(0)
        self.frame_left = Frame(self.root, borderwidth=10, height=360, width=350)
        self.frame_left.pack(side=LEFT)
        self.frame_left.pack_propagate(0)

        self.button_scrape = Button(
            self.frame_right, text="Scrape YT", width=50, command=self._clickYTScrape
        )
        self.button_scrape.pack(side=TOP)

        self.button_click = Button(
            self.frame_right,
            text="Click selection",
            width=50,
            command=self._clickClickSelection,
        )
        self.button_click.pack(side=TOP)

        self.button_quit = Button(
            self.frame_right, text="Quit", width=50, command=self.__del__
        )
        self.button_quit.pack(side=TOP, pady=30)

        self.listbox = Listbox(
            self.frame_left, selectmode=SINGLE, height=350, width=200
        )
        self.listbox.pack(side=BOTTOM)
        self.listbox.bind("<Double-Button-1>", self._clickClickSelection)

    def __del__(self):
        del self.scraper
        del self.db
        self.root.destroy()

    def run(self):
        self.root.mainloop()

    def _clickYTScrape(self):
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
            self.listbox.insert(END, title)

        self.ft.incTrain(tuple(links))
        self.click_prob = self.ft.similScraped2Clicked(tuple(links))

    def _clickClickSelection(self):
        """Simulate user click on video and print scores.

        Pass selected link to Browser object, i.e. selenium.
        Print scores and whether selection was probable next click.
        """
        sel = self.listbox.curselection()
        if sel:
            link = self.records[sel[0]][0]
            self.browser.clickLink(link)
            self.db.updateClicked(link)

            argsort = np.argsort(-1 * np.array(self.click_prob))  # descending sort

            prob_sort = np.array(self.click_prob)[argsort]
            rec_sort = np.array(self.records)[argsort]

            if link in rec_sort[:5, 0]:
                print("\n+++ HIT! +++ Video was in 5 most probable.\n")
            else:
                print("\n--- MISS! --- Video was not in 5 most probable.\n")

            print(
                "##################\n" + "Scores and titles:\n" + "##################\n"
            )
            for tup in list(zip(prob_sort, rec_sort[:, 1])):
                print(tup)
