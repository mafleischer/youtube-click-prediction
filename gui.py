from tkinter import Tk, Frame


class GUI:
    def __init__(self):
        self.root = Tk()
        self.frame = Frame(self.root)

    def __del__(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()
