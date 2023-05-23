import tkinter as tk


class Sub(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.exists = True

        self.title("MKWii Text Generator")
        self.minsize(738, 176)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.canvas = tk.Canvas(self, width=0, height=0, highlightthickness=0)
        self.canvas.pack(anchor=tk.NW, padx=2, pady=2)

        if int(master.user_interface.checkbutton.value.get()):
            self.config(bg="#202020")
            self.canvas.config(bg="#202020")

    def close(self):
        self.exists = False
        self.withdraw()

    def adjust_position(self):
        self.update()
        self.lower(self.master)
        self.master.geometry(
            f"+{self.winfo_x() + self.winfo_width() - 236}+{self.winfo_y() + 120}"
        )
