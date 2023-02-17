import re
from pathlib import Path

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from PIL import ImageTk

from app_package.menu_bar import MenuBar
from app_package.widget import ColorWidget, ColorfulWidget, GradientWidget
from app_package.text_generator import TextGenerator


def main():
    app = App()
    app.mainloop()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MKWii Text Generator")
        self.minsize(675, 0)
        self.resizable(False, False)

        if Path("Fonts/icon.png").exists():
            self.iconphoto(True, tk.PhotoImage(file="Fonts/icon.png"))

        self.canvas = tk.Canvas(self, width=0, height=0, highlightthickness=0)
        self.canvas.pack(anchor=tk.NW, side=tk.LEFT)
        self.user_interface = UserInterface(self)
        self.user_interface.pack(anchor=tk.NE, padx=2, pady=2)

        menu_bar = MenuBar(self)
        self.config(menu=menu_bar)

        self.bind("<Alt-F4>", lambda event: None)  # <Key> を外す


class UserInterface(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.canvas = master.canvas
        master.bind("<Key>", self.change_text)  # キー入力で実行する

        self.text = ScrolledText(self, width=30, height=6, undo=True)
        self.text.grid(columnspan=2)
        self.text.focus_set()
        self.text.bind("<Tab>", self.tab)
        self.text.bind("<Control-a>", self.ctrl_a)

        # self.file_names
        self.file_names = self.to_file_names(self.text.get("1.0", "end-1c"))

        # self.var_scale.get() / 10 + 1
        self.var_scale = tk.IntVar()
        self.scale_value_label = tk.Label(self, text=self.var_scale.get() * 5)
        self.scale_value_label.grid(row=1, column=0)
        scale = ttk.Scale(
            self, orient=tk.HORIZONTAL, to=20,
            variable=self.var_scale, command=self.change_scale,
        )
        scale.grid(row=1, column=1, sticky=tk.EW)

        # self.var_combobox.get()
        self.var_combobox = tk.StringVar()
        combobox = ttk.Combobox(
            self, justify="center", state="readonly",
            height=5, textvariable=self.var_combobox,
            values=("Yellow", "White", "Color", "Colorful", "Gradient"),
        )
        combobox.grid(columnspan=2, sticky=tk.EW)
        combobox.current(0)
        combobox.bind("<<ComboboxSelected>>", self.change_widget)

        self.create_nest_widget()

    def to_file_names(self, text_area) -> list:
        replace_dict = {":": "CORON", ".": "PERIOD", "/": "SLASH", " ": "SPACE"}
        file_names = [replace_dict.get(char, char) for char in text_area.upper()]

        count, need_replace = 0, False  # 「'」間の文字を置換
        for i, file_name in enumerate(file_names):
            if file_name == "'" and count < file_names.count("'") // 2:
                if not need_replace:
                    need_replace = True
                else:
                    need_replace = False
                    count += 1
            elif need_replace and file_name in [*map(str, range(10)), "-", "SLASH", "SPACE"]:
                file_names[i] += "_"

        # 使用できない文字がないか検証
        file_names = [
            file_name
            for file_name in file_names
            if re.sub("[^-+0-9A-Z\n]", "", file_name)
        ]
        # 右側の空白と改行を削除
        while len(file_names) and file_names[-1] in ["SPACE", "SPACE_", "\n"]:
            del file_names[-1]

        return file_names

    def create_nest_widget(self):
        self.nest_widget = tk.Frame(self)
        self.nest_widget.grid(columnspan=2, sticky=tk.W)

        self.color_widget = ColorWidget(self)
        self.colorful_widget = ColorfulWidget(self)
        self.gradient_widget = GradientWidget(self)

    def change_text(self, event):
        # 「file_names」を更新
        self.file_names = self.to_file_names(self.text.get("1.0", "end-1c"))
        # 「Colorful」のコンボボックスを更新
        self.colorful_widget.label_combobox.combobox.config(values=self.file_names)
        if len(self.file_names):
            self.colorful_widget.label_combobox.combobox.current(0)
            self.colorful_widget.change_colorful_combobox()

        self.change_widget()  # 「Colorful」の「len(self.file_names)」に対応させる

    def change_scale(self, event):
        # 輝度の表示
        self.scale_value_label.config(text=self.var_scale.get() * 5)
        self.update_canvas()

    def change_widget(self, event=None):
        self.nest_widget.grid_forget()

        if self.var_combobox.get() == "Color":
            self.nest_widget = self.color_widget
        elif self.var_combobox.get() == "Colorful" and len(self.file_names):
            self.nest_widget = self.colorful_widget
        elif self.var_combobox.get() == "Gradient":
            self.nest_widget = self.gradient_widget
        else:
            self.nest_widget = tk.Frame(self)

        self.nest_widget.grid(columnspan=2, sticky=tk.W)

        if event:  # コンボボックスが変更されたとき、「Vertical」に戻す
            self.gradient_widget.var_radio.set(0)
            self.gradient_widget.change_label_when_vertical()
        else:
            self.update_canvas()

    def update_canvas(self, event=None):
        text_generator = TextGenerator(self)
        self.PIL_MKWii_text = text_generator.generate_image()
        self.Tk_MKWii_text = ImageTk.PhotoImage(self.PIL_MKWii_text)

        self.canvas.config(
            width=self.Tk_MKWii_text.width() + 2,
            height=self.Tk_MKWii_text.height() + 2,
        )
        self.canvas.create_image(2, 2, anchor=tk.NW, image=self.Tk_MKWii_text)

    def tab(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def ctrl_a(self, event):
        self.text.tag_add(tk.SEL, "1.0", "end-1c")
        return "break"


if __name__ == "__main__":
    main()
