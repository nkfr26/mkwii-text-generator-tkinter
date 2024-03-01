import tkinter as tk

from .app.user_interface import UserInterface
from .app.menu import Menu
from .app.sub import Sub


def main():
    application = Application()
    application.mainloop()


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("")
        self.resizable(False, False)

        self.user_interface = UserInterface(self)
        self.user_interface.pack(anchor=tk.NE, padx=2, pady=2)

        self.menu = Menu(self)
        self.config(menu=self.menu)

        self.sub = Sub(self)
        self.sub.adjust_position()
        self.sub.bind("<Control-e>", self.menu.export)
        self.sub.bind("<Control-o>", self.menu.open_png_folder)
