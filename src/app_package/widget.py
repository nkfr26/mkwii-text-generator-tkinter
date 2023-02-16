import tkinter as tk

from .widget_package.parts import (
    ColorLabelButton, TopColorLabelButton, BtmColorLabelButton,
    ColorfulLabelButton, ColorfulLabelCombobox,
)


class ParentNestWidget(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master


class ColorWidget(ParentNestWidget):
    def __init__(self, master):
        super().__init__(master)
        self.label_button = ColorLabelButton(self)
        self.label_button.grid(row=1, column=0)


class ColorfulWidget(ParentNestWidget):
    def __init__(self, master):
        super().__init__(master)
        self.label_button = ColorfulLabelButton(self)
        self.label_button.grid(row=1, column=0)

        self.label_combobox = ColorfulLabelCombobox(self)
        self.label_combobox.grid(row=1, column=1)

        self.label_combobox.combobox.bind(
            "<<ComboboxSelected>>", self.change_colorful_combobox
        )

    def change_colorful_combobox(self, event=None):
        index = self.label_combobox.combobox.current()
        self.label_button.button.i = index
        self.label_button.button.config(bg=self.label_button.button.colors[index])


class GradientWidget(ParentNestWidget):
    def __init__(self, master):
        super().__init__(master)
        # self.var_radio.get()
        self.var_radio = tk.IntVar()
        vertical_radio = tk.Radiobutton(
            self, value=0, variable=self.var_radio,
            text="Vertical", command=self.change_label_when_vertical,
        )
        vertical_radio.grid(row=0, column=0, sticky=tk.W)
        horizontal_radio = tk.Radiobutton(
            self, value=1, variable=self.var_radio,
            text="Horizontal", command=self.change_label_when_horizontal,
        )
        horizontal_radio.grid(row=0, column=1, sticky=tk.W)

        self.left_label_button = TopColorLabelButton(self)
        self.left_label_button.grid(row=1, column=0)
        self.right_label_button = BtmColorLabelButton(self)
        self.right_label_button.grid(row=1, column=1)

    def change_label_when_vertical(self):
        self.master.update_canvas()
        self.left_label_button.label.config(text="Top")
        self.right_label_button.label.config(text="Bottom")

    def change_label_when_horizontal(self):
        self.master.update_canvas()
        self.left_label_button.label.config(text="Left")
        self.right_label_button.label.config(text="Right")
