import tkinter as tk
import tkinter.ttk as ttk


class ScrollableFrame(tk.Frame):
    def __init__(self, master: tk.Misc):
        super().__init__(master)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=98)
        self.columnconfigure(1, weight=2)

        self.canvas = tk.Canvas(self, width=1, height=1)
        self.vscroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.vscroll.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=self.vscroll.set)
        self.canvas.bind('<Configure>', lambda _: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.inner_frame = tk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

