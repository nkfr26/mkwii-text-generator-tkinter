import tkinter as tk
from tkinter import ttk

from .picker import SinglePicker, MultiPicker, TopPicker, BtmPicker


class Base(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.propagate(False)
        self.config(width=116, height=42)


class SPFrame(Base):
    def __init__(self, master):
        super().__init__(master)
        self.config(text="Color")

        self.button = SinglePicker(self)
        self.button.pack(side=tk.LEFT, padx=6)


class MPFrame(Base):
    def __init__(self, master):
        super().__init__(master)
        self.config(text="Color")

        self.button = MultiPicker(self)
        self.button.pack(side=tk.LEFT, padx=6)


class MCFrame(Base):
    def __init__(self, master):
        super().__init__(master)
        self.config(text="Character")

        self.combobox = ttk.Combobox(
            self, justify="center", state="readonly", takefocus=False
        )
        self.combobox.pack(fill=tk.X, padx=6)
        self.combobox.bind("<<ComboboxSelected>>", master.on_change)


class TPFrame(Base):
    def __init__(self, master):
        super().__init__(master)
        self.config(text="Top")

        self.button = TopPicker(self)
        self.button.pack(side=tk.LEFT, padx=6)


class BPFrame(Base):
    def __init__(self, master):
        super().__init__(master)
        self.config(text="Bottom")

        self.button = BtmPicker(self)
        self.button.pack(side=tk.LEFT, padx=6)


class Orientation(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.config(text="Orientation")

        self.value = tk.IntVar()
        vertical = tk.Radiobutton(
            self, value=0, text="Vertical",
            variable=self.value, command=self.on_change, takefocus=False,
        )
        vertical.pack(anchor=tk.W)
        horizontal = tk.Radiobutton(
            self, value=1, text="Horizontal",
            variable=self.value, command=self.on_change, takefocus=False,
        )
        horizontal.pack(anchor=tk.W)

    def on_change(self):
        if self.value.get() == 0:
            self.master.tpframe.config(text="Top")
            self.master.bpframe.config(text="Bottom")
        else:
            self.master.tpframe.config(text="Left")
            self.master.bpframe.config(text="Right")

        self.master.master.update_canvas()


class Mode(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.config(text="Mode")

        self.value = tk.IntVar()
        rgb = tk.Radiobutton(
            self, value=0, text="RGB",
            variable=self.value, command=self.on_change, takefocus=False,
        )
        rgb.pack(anchor=tk.W)
        hsl = tk.Radiobutton(
            self, value=1, text="HSL",
            variable=self.value, command=self.on_change, takefocus=False,
        )
        hsl.pack(anchor=tk.W)

    def on_change(self):
        self.master.master.update_canvas()
