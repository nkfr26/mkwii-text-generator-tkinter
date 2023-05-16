import tkinter as tk

from PIL import ImageTk

from app_package.menu_bar import MenuBar
from app_package.sub import Sub
from app_package.widget import Text, Scale, Checkbutton, Combobox
from app_package.option import Single, Multi, Gradient
from app_package.text_image_generator import TextImageGenerator


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

        menu = MenuBar(self)
        self.config(menu=menu)

        self.sub = Sub(self)
        self.sub.bind("<Control-e>", menu.export)
        self.sub.bind("<Control-o>", menu.open_png_folder)
        self.sub.adjust_position()

        self.bind("<Alt-F4>", lambda event: None)  # <Key> を外す


class UserInterface(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # self.text.file_names
        self.text = Text(self)
        self.text.grid(columnspan=2, sticky=tk.EW)
        master.bind("<Key>", self.text.on_change)  # キー入力で実行する

        # self.scale.value.get() / 10 + 1
        self.scale = Scale(self)
        self.scale.grid(row=1, column=0)

        # self.checkbutton.value.get()
        self.checkbutton = Checkbutton(self)
        self.checkbutton.grid(row=1, column=1, sticky=tk.NS)

        # self.combobox.value.get()
        self.combobox = Combobox(self)
        self.combobox.grid(columnspan=2, sticky=tk.EW)

        self.create_option()

    def create_option(self):
        self.option = tk.Frame(self)
        self.option.grid(columnspan=2)

        self.single = Single(self)
        self.multi = Multi(self)
        self.gradient = Gradient(self)

    def change_widget(self, event=None):
        self.option.grid_forget()

        widget_mapping = {
            "Single Color": self.single,
            "Multi Color": self.multi if self.text.file_names else tk.Frame(self),
            "Gradient": self.gradient,
        }
        self.option = widget_mapping.get(self.combobox.value.get(), tk.Frame(self))
        self.option.grid(columnspan=2, sticky=tk.W)

        self.update_canvas()

    def update_canvas(self):
        text_image_generator = TextImageGenerator(self)
        self.PIL_MKWii_text = text_image_generator.generate_image()
        self.Tk_MKWii_text = ImageTk.PhotoImage(self.PIL_MKWii_text)

        sub_created = False
        if not self.master.sub.exists:
            self.master.sub.deiconify()
            self.text.focus_set()
            self.master.sub.exists = sub_created = True

        self.master.sub.canvas.config(
            width=self.Tk_MKWii_text.width(), height=self.Tk_MKWii_text.height()
        )
        self.master.sub.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.Tk_MKWii_text
        )

        if sub_created:
            self.master.sub.adjust_position()


if __name__ == "__main__":
    main()
