import tkinter as tk

from .user_interface import UserInterface
from .user_interface_package.menu import Menu
from .user_interface_package.sub import Sub


def main():
    app = App()
    app.mainloop()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("")
        self.resizable(False, False)

        self.user_interface = UserInterface(self)
        self.user_interface.pack(anchor=tk.NE, padx=2, pady=2)

        menu = Menu(self)
        self.config(menu=menu)

        self.sub = Sub(self)
        self.sub.bind("<Control-e>", menu.export)
        self.sub.bind("<Control-o>", menu.open_png_folder)
        self.sub.adjust_position()
