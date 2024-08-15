from book import Book


import tkinter as tk


class AddBooksBooklistWindow(tk.Toplevel):
    def __init__(self, master: tk.Tk, books: list[Book]):
        super().__init__(master)

        self.books = books
        self.books_to_add: list[Book] = []
