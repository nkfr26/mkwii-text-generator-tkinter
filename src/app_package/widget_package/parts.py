import tkinter as tk
from tkinter import ttk

from .color_button import (
    ColorButton, TopColorButton, BtmColorButton, ColorfulButton
)


class ParentLabelButton(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.config(width=115, height=42)
        self.grid_propagate(False)

        self.label = tk.Label(self)
        self.label.grid(row=0, padx=2)


class ColorLabelButton(ParentLabelButton):
    def __init__(self, master):
        super().__init__(master)
        self.label.config(text="Pick a color")

        self.button = ColorButton(self)
        self.button.grid(row=1, sticky=tk.W, padx=5)


class TopColorLabelButton(ParentLabelButton):
    def __init__(self, master):
        super().__init__(master)
        self.label.config(text="Top")

        self.button = TopColorButton(self)
        self.button.grid(row=1, sticky=tk.W, padx=5)


class BtmColorLabelButton(ParentLabelButton):
    def __init__(self, master):
        super().__init__(master)
        self.label.config(text="Bottom")

        self.button = BtmColorButton(self)
        self.button.grid(row=1, sticky=tk.W, padx=5)


class ColorfulLabelButton(ParentLabelButton):
    def __init__(self, master):
        super().__init__(master)
        self.label.config(text="Pick a color")

        self.button = ColorfulButton(self)
        self.button.grid(row=1, sticky=tk.W, padx=5)


class ColorfulLabelCombobox(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.config(width=116, height=42)
        self.grid_propagate(False)
        self.columnconfigure(0, weight=True)

        label = tk.Label(self, text="Select the character")
        label.grid(row=0, sticky=tk.W)

        self.combobox = ttk.Combobox(self, justify="center", state="readonly")
        self.combobox.grid(row=1, sticky=tk.EW)
