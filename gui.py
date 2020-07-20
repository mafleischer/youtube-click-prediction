from tkinter import Tk, Frame, Button, Listbox
from tkinter import RIGHT, LEFT, TOP, BOTTOM, END
from tkinter import SINGLE

from db_lang_workers import Work


def fn():
    pass


class GUI:
    def __init__(self, browser, scraper, db):
        self.browser = browser
        self.scraper = scraper
        self.db = db
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
        self.listbox.delete(0, END)
        tninfo = self.scraper.getTNVideoInfo()
        work = Work(self.db)
        work.filterRecords(tninfo)
        work.processWriteToDB(tninfo)
        self.records = tninfo
        self.listbox.delete(0, END)
        for rec in tninfo:
            title = rec[1]
            self.listbox.insert(END, title)

    def clickClickSelection(self):
        sel = self.listbox.curselection()
        if sel:
            link = self.records[sel[0]][0]
            self.browser.clickLink(link)
            self.db.updateClicked(link)
