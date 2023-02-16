import tkinter as tk
from tkinter import colorchooser


class ParentColorButton(tk.Button):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.image = tk.PhotoImage(width=12, height=12)
        self.config(image=self.image, command=self.color_change)

    def color_change(self):
        self.master.master.master.update_canvas()


class ColorButton(ParentColorButton):
    def __init__(self, master):
        super().__init__(master)
        self.color = "#f00"
        self.config(bg=self.color)

    def color_change(self):
        temp = self.color
        self.color = colorchooser.askcolor(temp)[1]
        if self.color is None:
            self.color = temp
        else:
            self.config(bg=self.color)
            super().color_change()


class TopColorButton(ParentColorButton):
    def __init__(self, master):
        super().__init__(master)
        self.top_color = "#0f0"
        self.config(bg=self.top_color)

    def color_change(self):
        temp = self.top_color
        self.top_color = colorchooser.askcolor(temp)[1]
        if self.top_color is None:
            self.top_color = temp
        else:
            self.config(bg=self.top_color)
            super().color_change()


class BtmColorButton(ParentColorButton):
    def __init__(self, master):
        super().__init__(master)
        self.btm_color = "#00f"
        self.config(bg=self.btm_color)

    def color_change(self):
        temp = self.btm_color
        self.btm_color = colorchooser.askcolor(temp)[1]
        if self.btm_color is None:
            self.btm_color = temp
        else:
            self.config(bg=self.btm_color)
            super().color_change()


class ColorfulButton(ParentColorButton):
    def __init__(self, master):
        super().__init__(master)
        self.i = 0
        self.colors = ["#fff" for _ in range(10000)]
        self.config(bg=self.colors[self.i])

    def color_change(self):
        temp = self.colors[self.i]
        self.colors[self.i] = colorchooser.askcolor(temp)[1]
        if self.colors[self.i] is None:
            self.colors[self.i] = temp
        else:
            self.config(bg=self.colors[self.i])
            super().color_change()
