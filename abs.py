from book import Book
from booklist import Booklist
from bookshelf import Bookshelf
from edit_book_window import EditBookWindow
from scrollable_treeview import ScrollableTreeview


import copy
import tkinter as tk
import tkinter.messagebox as msgbox
import tkinter.ttk as ttk


class ABS:
    def __init__(self, bookshelf: Bookshelf):
        self.bookshelf = bookshelf
        self.selected_booklist: Booklist = bookshelf.booklists["All Books"]

        self.root = tk.Tk()
        self.root.title("Aurora's Bookshelf")
        self.root.geometry("1200x600")

        self.__create_menu_bar()
        
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=22)
        self.root.columnconfigure(1, weight=5)
        self.root.columnconfigure(2, weight=73)

        self.__create_booklist_frame()

        # Vertical separator
        self.separator = ttk.Separator(self.root, orient="vertical")
        self.separator.grid(row=0, column=1)

        self.__create_books_frame()

        # Add booklists to the listbox and select the "All Books" list.
        self.repopulate_bookslists()
        self.listbox_booklists.selection_set(0)
        self.listbox_booklists.activate(0)

        # Setup the treeview columns and the search filters
        self.update_properties()

        self.repopulate_books()

    def __create_menu_bar(self):
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
        self.frame_booklists.grid(row=0, column=0, sticky="nsew")

        self.frame_booklists.rowconfigure(0, weight=5)
        self.frame_booklists.rowconfigure(1, weight=85)
        self.frame_booklists.rowconfigure(2, weight=10)
        self.frame_booklists.columnconfigure(0, weight=1)

        self.label_booklist_frame_title = tk.Label(self.frame_booklists, text="Booklists")
        self.label_booklist_frame_title.grid(row=0, column=0)
        
        self.listbox_booklists = tk.Listbox(self.frame_booklists)
        self.listbox_booklists.bind("<<ListboxSelect>>", lambda e: self.listbox_booklists_selection_changed(self.listbox_booklists.curselection()))
        self.listbox_booklists.grid(row=1, column=0, sticky="nsew", padx=5)

        # Booklist buttons frame
        self.frame_booklist_buttons = tk.Frame(self.frame_booklists)
        self.frame_booklist_buttons.grid(row=2, column=0, sticky="nsew")

        self.frame_booklist_buttons.rowconfigure(0, weight=1)
        self.frame_booklist_buttons.columnconfigure(0, weight=33)
        self.frame_booklist_buttons.columnconfigure(1, weight=33)
        self.frame_booklist_buttons.columnconfigure(2, weight=33)

        self.button_new_booklist = tk.Button(self.frame_booklist_buttons, text="New Booklist")
        self.button_new_booklist.grid(row=0, column=0, padx=5, sticky="ew")
        
        self.button_rename_booklist = tk.Button(self.frame_booklist_buttons, text="Rename Booklist")
        self.button_rename_booklist.grid(row=0, column=1, padx=5, sticky="ew")
        
        self.button_delete_booklist = tk.Button(self.frame_booklist_buttons, text="Delete Booklist")
        self.button_delete_booklist.grid(row=0, column=2, padx=5, sticky="ew")
        
    def __create_books_frame(self):
        self.frame_books = tk.Frame(self.root)
        self.frame_books.grid(row=0, column=2, sticky="nsew")

        self.frame_books.rowconfigure(0, weight=10)
        self.frame_books.rowconfigure(1, weight=80)
        self.frame_books.rowconfigure(2, weight=10)
        self.frame_books.columnconfigure(0, weight=1)

        # Search frame
        self.frame_search = tk.Frame(self.frame_books)
        self.frame_search.grid(row=0, column=0, sticky="nsew")

        self.frame_search.rowconfigure(0, weight=1)
        self.frame_search.columnconfigure(0, weight=10)
        self.frame_search.columnconfigure(1, weight=70)
        self.frame_search.columnconfigure(2, weight=10)
        self.frame_search.columnconfigure(3, weight=10)

        self.label_search = tk.Label(self.frame_search, text="Search:")
        self.label_search.grid(row=0, column=0, sticky="ew")

        self.entry_search = tk.Entry(self.frame_search)
        self.entry_search.grid(row=0, column=1, sticky="ew")

        self.to_filter = tk.StringVar(self.frame_search)
        self.to_filter.set("Title")

        options = ["TItle", "Author", "Publication Year"]

        self.options_search = tk.OptionMenu(self.frame_search, self.to_filter, *options)
        self.options_search.grid(row=0, column=2, sticky="ew")

        self.button_search = tk.Button(self.frame_search, text="Search")
        self.button_search.grid(row=0, column=3, sticky="ew")

        # Books Treeview
        self.scrollable_treeview_books = ScrollableTreeview(self.frame_books)
        self.scrollable_treeview_books.grid(row=1, column=0, sticky="nsew")

        self.treeview_books = self.scrollable_treeview_books.treeview

        # Books buttons frame
        self.frame_books_buttons = tk.Frame(self.frame_books)
        self.frame_books_buttons.grid(row=2, column=0, sticky="nse")

        self.frame_books_buttons.rowconfigure(0, weight=1)
        self.frame_books_buttons.columnconfigure(0, weight=33)
        self.frame_books_buttons.columnconfigure(1, weight=33)
        self.frame_books_buttons.columnconfigure(2, weight=33)

        self.button_new_book = tk.Button(self.frame_books_buttons, text="New Book", command=self.button_new_book_clicked)
        self.button_new_book.grid(row=0, column=0, sticky="e", padx=5)
        self.button_edit_book = tk.Button(self.frame_books_buttons, text="Edit Book", command=self.button_edit_book_clicked)
        self.button_edit_book.grid(row=0, column=1, sticky="e", padx=5)
        self.button_delete_book = tk.Button(self.frame_books_buttons, text="Delete Book")
        self.button_delete_book.grid(row=0, column=2, sticky="e", padx=5)

    def listbox_booklists_selection_changed(self, selected_item: tuple[int]):
        if not selected_item:
            return
        
        self.selected_booklist = self.bookshelf.booklists[self.listbox_booklists.get(selected_item[0])]
        self.repopulate_books()

    def repopulate_bookslists(self):
        for booklist in self.bookshelf.booklists.keys():
            self.listbox_booklists.insert(tk.END, booklist)

    def repopulate_books(self):
        for item in self.treeview_books.get_children():
            self.treeview_books.delete(item)

        for book_id in self.selected_booklist.books:
            book = self.bookshelf.books[book_id]
            self.treeview_books.insert("", "end",
                                       text=str(book_id),
                                       values=([book.title, book.author, book.publication_year] + [*book.custom_properties.values()]))
    
    def reconfigure_treeview_columns(self, columns: list[str]):
        self.treeview_books.configure(columns=columns)
        for column in columns:
            self.treeview_books.heading(column, text=column)
            self.treeview_books.column(column, width=150, stretch=True)

    def reconfigure_filters(self, filters: list[str]):
        menu: tk.Menu = self.options_search["menu"]
        menu.delete(0, "end")
        for filter in filters:
            menu.add_command(label=filter, command=tk._setit(self.to_filter, filter))

    def update_properties(self):
        all_properties = self.bookshelf.built_in_properties + self.bookshelf.custom_properties
        self.reconfigure_treeview_columns(all_properties)
        self.reconfigure_filters(all_properties)

    def show_window(self):
        self.root.mainloop()

    def button_new_book_clicked(self):
        """Display the window to create a new book or add a book to a booklist"""
        book = Book("", "", 0, *self.bookshelf.custom_properties)

        edit_book_window = EditBookWindow(self.root, book)
        self.root.wait_window(edit_book_window)

        if edit_book_window.confirmed:
            self.bookshelf.add_book(edit_book_window.book)

        self.repopulate_books()

    def button_edit_book_clicked(self):
        selected_items = self.treeview_books.selection()
        if not selected_items:
            msgbox.showerror("Select a Book", "Please select a book to edit")
            return
        
        selected_item = selected_items[0]
        selected_book_id = int(self.treeview_books.item(selected_item)["text"])
        book = copy.deepcopy(self.bookshelf.books[selected_book_id])
        
        edit_book_window = EditBookWindow(self.root, book)
        self.root.wait_window(edit_book_window)

        if edit_book_window.confirmed:
            self.bookshelf.books[selected_book_id] = edit_book_window.book

        self.repopulate_books()         
