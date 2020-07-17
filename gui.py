from tkinter import Tk, Frame, Button, Listbox
from tkinter import RIGHT, LEFT, TOP, BOTTOM, END
from tkinter import SINGLE


def fn():
    pass


class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("YouTube - Predict next click")

        self.frame_right = Frame(self.root, borderwidth=10, height=360, width=200)
        self.frame_right.pack(side=RIGHT)
        self.frame_right.pack_propagate(0)
        self.frame_left = Frame(self.root, borderwidth=10, height=360, width=200)
        self.frame_left.pack(side=LEFT)
        self.frame_left.pack_propagate(0)

        self.button_scrape = Button(
            self.frame_right, text="Scrape YT", width=50, command=fn
        )
        self.button_scrape.pack(side=TOP)
        self.button_click = Button(
            self.frame_right, text="Click selection", width=50, command=fn
        )
        self.button_click.pack(side=TOP)

        self.listbox = Listbox(self.frame_left, selectmode=SINGLE, height=350)
        self.listbox.pack(side=BOTTOM)
        self.listbox.bind("<Double-Button-1>", fn)

        for item in range(22):
            self.listbox.insert(END, str(item))

    def __del__(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()
