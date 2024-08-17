from book import Book


import tkinter as tk


class Search(tk.Frame):
    def __init__(self, master: tk.Misc, default_options: list[str]):
        super().__init__(master)

        self.default_options = default_options

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
        self.to_filter.set(self.default_options[0])

        self.options_search = tk.OptionMenu(self, self.to_filter, *self.default_options)
        self.options_search.grid(row=0, column=2, sticky="ew")

        self.button_search = tk.Button(self, text="Search")
        self.button_search.grid(row=0, column=3, sticky="ew")

    def configure_filters(self, filters: list[str]):
        menu: tk.Menu = self.options_search["menu"]
        menu.delete(0, "end")
        for search_filter in filters:
            menu.add_command(label=search_filter, command=tk._setit(self.to_filter, search_filter))
    
    def filter_books(self, books: list[Book]) -> list[Book]:
        search_filter = self.to_filter.get()
        search_term = self.entry_search.get()

        if search_filter in self.default_options:
            # If the search filter is one of the built-in properties, we need to search the __dict__
            search_filter = search_filter.lower()
            search_filter = search_filter.replace(" ", "_")

            found_books = [book for book in books if search_term.casefold() in book.__dict__[search_filter].casefold()]
        else:
            found_books = [book for book in books if search_term.casefold() in book.custom_properties[search_filter].casefold()]

        return found_books
