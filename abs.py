import tkinter as tk


from bookshelf import Bookshelf
from tkinter import ttk


class ABS:
    def __init__(self, bookshelf: Bookshelf):
        self.bookshelf = bookshelf

        self.root = tk.Tk()
        self.root.title("Aurora's Bookshelf")

        self.__create_menu_bar()
        
        self.__create_booklist_frame()

        # Vertical separator
        self.separator = ttk.Separator(self.root, orient="vertical")
        self.separator.grid(row=0, column=1)

        self.__create_books_frame()

        self.root.mainloop()

    def __create_menu_bar(self):                # Menu bar
        self.menu_bar = tk.Menu(self.root)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open Bookshelf File Location")
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Edit Book Properties")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Help Menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About")
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.root.config(menu=self.menu_bar)

    def __create_booklist_frame(self):
        self.frame_booklists = tk.Frame(self.root)
        self.frame_booklists.grid(row=0, column=0)

        self.label_booklist_frame_title = tk.Label(self.frame_booklists, text="Booklists")
        self.label_booklist_frame_title.grid(row=0, column=0)
        self.listbox_booklists = tk.Listbox(self.frame_booklists)
        self.listbox_booklists.grid(row=1, column=0)

        # Booklist buttons frame
        self.frame_booklist_buttons = tk.Frame(self.frame_booklists)
        self.frame_booklist_buttons.grid(row=2, column=0)

        self.button_new_booklist = tk.Button(self.frame_booklist_buttons, text="New Booklist")
        self.button_new_booklist.grid(row=0, column=0)
        self.button_rename_booklist = tk.Button(self.frame_booklist_buttons, text="Rename Booklist")
        self.button_rename_booklist.grid(row=0, column=1)
        self.button_delete_booklist = tk.Button(self.frame_booklist_buttons, text="Delete Booklist")
        self.button_delete_booklist.grid(row=0, column=2)
    
    def __create_books_frame(self):
        self.frame_books = tk.Frame(self.root)
        self.frame_books.grid(row=0, column=2)

        # Search frame
        self.frame_search = tk.Frame(self.frame_books)
        self.frame_search.grid(row=0, column=0)

        self.label_search = tk.Label(self.frame_search, text="Search: ")
        self.label_search.grid(row=0, column=0)
        self.entry_search = tk.Entry(self.frame_search)
        self.entry_search.grid(row=0, column=1)

        self.to_filter = tk.StringVar(self.frame_search)
        self.to_filter.set("Title")

        # Temporary
        options = ["TItle", "Author", "Publication Year"]

        self.options_search = tk.OptionMenu(self.frame_search, self.to_filter, *options)
        self.options_search.grid(row=0, column=2)
        self.button_search = tk.Button(self.frame_search, text="Search")
        self.button_search.grid(row=0, column=3)

        self.treeview_books = ttk.Treeview(self.frame_books)
        self.treeview_books.grid(row=1, column=0)

        # Books buttons frame
        self.frame_books_buttons = tk.Frame(self.frame_books)
        self.frame_books_buttons.grid(row=2, column=0)

        self.button_new_book = tk.Button(self.frame_books_buttons, text="New Book")
        self.button_new_book.grid(row=0, column=0)
        self.button_edit_book = tk.Button(self.frame_books_buttons, text="Edit Book")
        self.button_edit_book.grid(row=0, column=1)
        self.button_delete_book = tk.Button(self.frame_books_buttons, text="Delete Book")
        self.button_delete_book.grid(row=0, column=2)
