import re

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class Text(ScrolledText):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.file_names = ""

        self.config(width=30, height=6, undo=True)
        self.focus_set()
        self.bind("<Tab>", self.tab)
        self.bind("<Control-a>", self.ctrl_a)
        self.bind("<Control-o>", self.ctrl_o)

    def tab(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def ctrl_a(self, event):
        self.tag_add(tk.SEL, "1.0", "end-1c")
        return "break"

    def ctrl_o(self, event):
        self.master.master.menu.open_png_folder()
        return "break"  # 改行しないようにする

    def on_change(self, event):
        # 「file_names」を更新
        self.file_names = self.to_file_names(self.get("1.0", "end-1c"))
        # 「Multi Color」のコンボボックスを更新
        self.master.multi.mcframe.combobox.config(values=self.file_names)
        if self.file_names:
            self.master.multi.mcframe.combobox.current(0)
            self.master.multi.on_change()
        # 「Multi Color」の「if self.file_names」に対応させる
        self.master.change_option()

    def to_file_names(self, text_area) -> list:
        replace_dict = {
            ":": "COLON", ".": "PERIOD", "/": "SLASH", " ": "SPACE", "<": "LEFT", ">": "RIGHT"
        }
        file_names = [replace_dict.get(char, char) for char in text_area.upper()]

        count, need_replace = 0, False  # 「"」間の文字を置換
        for i, file_name in enumerate(file_names):
            if file_name == '"' and count < file_names.count('"') // 2:
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
            if re.sub("[^-+0-9A-Z<>\n]", "", file_name)
        ]
        # 右側の空白と改行を削除
        while file_names and file_names[-1] in ["SPACE", "SPACE_", "\n", "LEFT", "RIGHT"]:
            del file_names[-1]

        return file_names


class Scale(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.propagate(False)
        self.config(width=174, height=45)

        self.value = tk.IntVar()
        self.config(text=f" {self.value.get() * 5} ")  # 輝度の表示 (5刻み)
        scale = ttk.Scale(
            self, orient=tk.HORIZONTAL, from_=-4, to=20,
            variable=self.value, command=self.on_change, takefocus=False,
        )
        scale.pack(fill=tk.X, padx=5)

    def on_change(self, event):
        self.config(text=f" {self.value.get() * 5} ")
        self.master.update_canvas()


class Checkbutton(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.config(text="Stroke", width=58)

        self.value = tk.BooleanVar()
        checkbutton = ttk.Checkbutton(
            self, text="White",
            variable=self.value, command=self.on_change, takefocus=False,
        )
        checkbutton.place(x=0, y=1)

    def on_change(self):
        self.master.update_canvas()

        if self.master.master.menu.bg_lock.get():
            pass
        elif self.value.get():
            self.master.master.sub.config(bg="#202020")
            self.master.master.sub.canvas.config(bg="#202020")
        else:
            self.master.master.sub.config(bg="SystemButtonFace")
            self.master.master.sub.canvas.config(bg="SystemButtonFace")


class Combobox(ttk.Combobox):
    def __init__(self, master):
        super().__init__(master)
        self.value = tk.StringVar()
        self.config(
            justify="center", state="readonly",
            textvariable=self.value, takefocus=False,
            values=("Yellow", "White", "Single Color", "Multi Color", "Gradient"),
        )
        self.current(0)
        self.bind("<<ComboboxSelected>>", master.change_option)
