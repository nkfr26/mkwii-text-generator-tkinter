import tkinter as tk

from PIL import ImageTk

from .ui.widget import Text, Scale, Checkbutton, Combobox
from .ui.option import Single, Multi, Gradient
from .feature.text_image_generator import TextImageGenerator


class UserInterface(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # self.text.file_names
        self.text = Text(self)
        self.text.grid(columnspan=2, sticky=tk.EW)
        master.bind("<Key>", self.text.on_change)
        master.bind("<Alt-F4>", lambda event: None)

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
        self.option.grid()

        self.single = Single(self)
        self.multi = Multi(self)
        self.gradient = Gradient(self)

    def change_option(self, event=None):
        self.option.grid_forget()

        option_mapping = {
            "Single Color": self.single,
            "Multi Color": self.multi if self.text.file_names else tk.Frame(self),
            "Gradient": self.gradient,
        }
        self.option = option_mapping.get(self.combobox.value.get(), tk.Frame(self))
        self.option.grid(columnspan=2, sticky=tk.W)

        self.update_canvas()

    def update_canvas(self):
        text_image_generator = TextImageGenerator(self)
        self.PIL_MKWii_text = text_image_generator.run()
        self.Tk_MKWii_text = ImageTk.PhotoImage(self.PIL_MKWii_text)

        sub_redrawn = False
        if not self.master.sub.exists:
            self.master.sub.deiconify()
            self.text.focus_set()
            sub_redrawn = self.master.sub.exists = True

        self.master.sub.canvas.config(
            width=self.Tk_MKWii_text.width(), height=self.Tk_MKWii_text.height()
        )
        self.master.sub.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.Tk_MKWii_text
        )

        if sub_redrawn:
            self.master.sub.adjust_position()
