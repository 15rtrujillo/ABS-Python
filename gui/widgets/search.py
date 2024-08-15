import tkinter as tk


class Search(tk.Frame):
    def __init__(self, master: tk.Misc):
        super().__init__(master)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=10)
        self.columnconfigure(1, weight=70)
        self.columnconfigure(2, weight=10)
        self.columnconfigure(3, weight=10)

        self.label_search = tk.Label(self, text="Search:")
        self.label_search.grid(row=0, column=0, sticky="ew")

        self.entry_search = tk.Entry(self)
        self.entry_search.grid(row=0, column=1, sticky="ew")

        self.to_filter = tk.StringVar(self)
        self.to_filter.set("Title")

        options = ["TItle", "Author", "Publication Year"]

        self.options_search = tk.OptionMenu(self, self.to_filter, *options)
        self.options_search.grid(row=0, column=2, sticky="ew")

        self.button_search = tk.Button(self, text="Search")
        self.button_search.grid(row=0, column=3, sticky="ew")
