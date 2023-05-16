import datetime
import subprocess
import webbrowser
from pathlib import Path

import tkinter as tk
from tkinter import filedialog


class MenuBar(tk.Menu):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        file = tk.Menu(self, tearoff=False)
        help = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File", menu=file)
        self.add_cascade(label="Help", menu=help)

        file.add_command(label="Export", command=self.export)
        file.add_command(label="Open PNG Folder", command=self.open_png_folder)

        help_readme = tk.Menu(help, tearoff=False)
        help_readme.add_command(label="English", command=self.open_readme_en)
        help_readme.add_command(label="日本語", command=self.open_readme_ja)

        help.add_cascade(label="README", menu=help_readme)
        help.add_command(label="GitHub", command=self.open_github)
        help.add_command(label="Developer's Twitter", command=self.open_twitter)

        master.bind("<Control-e>", self.export)
        master.bind("<Control-o>", self.open_png_folder)
        master.user_interface.text.bind("<Control-o>", self.unbind_text_ctrl_o)

    def export(self, event=None):
        if not self.master.user_interface.text.file_names:
            return

        Path("PNG").mkdir(exist_ok=True)

        path_name = filedialog.asksaveasfilename(
            initialdir="PNG", initialfile=datetime.date.today(),
            defaultextension="", filetypes=[("PNG", "*.png")],
        )
        if path_name:
            self.master.user_interface.PIL_MKWii_text.save(path_name)

    def open_png_folder(self, event=None):
        Path("PNG").mkdir(exist_ok=True)
        subprocess.run(["explorer", "PNG"])

    def unbind_text_ctrl_o(self, event):
        self.open_png_folder()
        return "break"

    def open_readme_en(self):
        subprocess.Popen(["C:/Windows/notepad.exe", "README/English.txt"])

    def open_readme_ja(self):
        subprocess.Popen(["C:/Windows/notepad.exe", "README/Japanese.txt"])

    def open_github(self):
        webbrowser.open("https://github.com/NOKKY726/mkwii-text-generator-tkinter/")

    def open_twitter(self):
        webbrowser.open("https://twitter.com/nkfrom_mkw/")
