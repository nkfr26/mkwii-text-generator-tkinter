import tkinter as tk
from tkinter.colorchooser import askcolor


class Picker(tk.Button):
    def __init__(self, master):
        super().__init__(master)

        self.image = tk.PhotoImage(width=12, height=12)
        self.config(image=self.image, command=self.on_change, takefocus=False)

    def on_change(self):  # オーバーライドする
        pass

    def update_canvas(self):
        self.master.master.master.update_canvas()


class SinglePicker(Picker):
    def __init__(self, master):
        super().__init__(master)
        self.color = "#ff0000"
        self.config(bg=self.color)

    def on_change(self):
        temp = self.color
        self.color = askcolor(temp)[1]
        if self.color is None:
            self.color = temp
        else:
            self.config(bg=self.color)
            super().update_canvas()


class MultiPicker(Picker):
    def __init__(self, master):
        super().__init__(master)
        self.i = 0
        self.colors = ["#ffffff" for _ in range(10**4)]
        self.config(bg=self.colors[self.i])

    def on_change(self):
        temp = self.colors[self.i]
        self.colors[self.i] = askcolor(temp)[1]
        if self.colors[self.i] is None:
            self.colors[self.i] = temp
        else:
            self.config(bg=self.colors[self.i])
            super().update_canvas()


class TopPicker(Picker):
    def __init__(self, master):
        super().__init__(master)
        self.color = "#00ff00"
        self.config(bg=self.color)

    def on_change(self):
        temp = self.color
        self.color = askcolor(temp)[1]
        if self.color is None:
            self.color = temp
        else:
            self.config(bg=self.color)
            super().update_canvas()


class BtmPicker(Picker):
    def __init__(self, master):
        super().__init__(master)
        self.color = "#0000ff"
        self.config(bg=self.color)

    def on_change(self):
        temp = self.color
        self.color = askcolor(temp)[1]
        if self.color is None:
            self.color = temp
        else:
            self.config(bg=self.color)
            super().update_canvas()
