import tkinter as tk

from .opt.parts import (
    SPFrame, MPFrame, MCFrame,
    Orientation, Mode, TPFrame, BPFrame,
)


class Single(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.spframe = SPFrame(self)
        self.spframe.pack()


class Multi(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.mpframe = MPFrame(self)
        self.mpframe.grid(row=0, column=0)

        self.mcframe = MCFrame(self)
        self.mcframe.grid(row=0, column=1)

    def on_change(self, event=None):
        index = self.mcframe.combobox.current()
        self.mpframe.button.i = index
        self.mpframe.button.config(bg=self.mpframe.button.colors[index])


class Gradient(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.orientation = Orientation(self)
        self.orientation.grid(row=0, column=0, sticky=tk.EW)
        self.mode = Mode(self)
        self.mode.grid(row=0, column=1, sticky=tk.EW)

        self.tpframe = TPFrame(self)
        self.tpframe.grid(row=1, column=0)
        self.bpframe = BPFrame(self)
        self.bpframe.grid(row=1, column=1)
