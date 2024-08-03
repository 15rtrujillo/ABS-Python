import tkinter as tk
import tkinter.ttk as ttk


class ScrollableTreeview(tk.Frame):
    def __init__(self, master: tk.Misc):
        super().__init__(master)

        self.rowconfigure(0, weight=98)
        self.rowconfigure(1, weight=2)
        self.columnconfigure(0, weight=98)
        self.columnconfigure(1, weight=2)

        self.treeview = ttk.Treeview(self, show="headings")

        # Scrollbars
        self.hscroll = ttk.Scrollbar(self, orient="horizontal", command=self.treeview.xview)
        self.vscroll = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)

        self.treeview.configure(xscrollcommand=self.hscroll.set, yscrollcommand=self.vscroll.set)

        self.treeview.grid(row=0, column=0, sticky="nsew")
        self.vscroll.grid(row=0, column=1, sticky="ns")
        self.hscroll.grid(row=1, column=0, sticky="ew")