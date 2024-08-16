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

        self.default_options = ["Title", "Author", "Publication Year"]

        self.options_search = tk.OptionMenu(self, self.to_filter, *self.default_options)
        self.options_search.grid(row=0, column=2, sticky="ew")

        self.button_search = tk.Button(self, text="Search")
        self.button_search.grid(row=0, column=3, sticky="ew")

    def configure_filters(self, filters: list[str]):
        menu: tk.Menu = self.options_search["menu"]
        menu.delete(0, "end")
        for search_filter in filters:
            menu.add_command(label=search_filter, command=tk._setit(self.to_filter, search_filter))
