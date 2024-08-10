from gui.about_window import AboutWindow
from book import Book
from booklist import Booklist
from bookshelf import Bookshelf
from gui.edit_book_window import EditBookWindow
from gui.name_booklist_window import NameBooklistWindow
from gui.widgets.scrollable_listbox import ScrollableListbox
from gui.widgets.scrollable_treeview import ScrollableTreeview


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
        self.help_menu.add_command(label="About", command=lambda: AboutWindow(self.root))
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
        
        self.scrollable_listbox_booklists = ScrollableListbox(self.frame_booklists)
        self.scrollable_listbox_booklists.grid(row=1, column=0, sticky="nsew", padx=5)

        self.listbox_booklists = self.scrollable_listbox_booklists.listbox
        self.listbox_booklists.bind("<<ListboxSelect>>", lambda _: self.listbox_booklists_selection_changed())

        # Booklist buttons frame
        self.frame_booklist_buttons = tk.Frame(self.frame_booklists)
        self.frame_booklist_buttons.grid(row=2, column=0, sticky="nsew")

        self.frame_booklist_buttons.rowconfigure(0, weight=1)
        self.frame_booklist_buttons.columnconfigure(0, weight=33)
        self.frame_booklist_buttons.columnconfigure(1, weight=33)
        self.frame_booklist_buttons.columnconfigure(2, weight=33)

        self.button_new_booklist = tk.Button(self.frame_booklist_buttons, text="New Booklist", command=self.button_new_booklist_clicked)
        self.button_new_booklist.grid(row=0, column=0, padx=5, sticky="ew")
        
        self.button_rename_booklist = tk.Button(self.frame_booklist_buttons, text="Rename Booklist", command=self.button_rename_booklist_clicked)
        self.button_rename_booklist.grid(row=0, column=1, padx=5, sticky="ew")
        
        self.button_delete_booklist = tk.Button(self.frame_booklist_buttons, text="Delete Booklist", command=self.button_delete_booklist_clicked)
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
        self.button_delete_book = tk.Button(self.frame_books_buttons, text="Delete Book", command=self.button_delete_book_clicked)
        self.button_delete_book.grid(row=0, column=2, sticky="e", padx=5)

    def get_selected_booklist_name(self) -> str | None:
        selected_items = self.listbox_booklists.curselection()

        if not selected_items:
            return None
        
        return self.listbox_booklists.get(selected_items[0])


    def listbox_booklists_selection_changed(self):   
        selected_booklist_name = self.get_selected_booklist_name()
        if selected_booklist_name is None:
            return
        
        selected_booklist = self.bookshelf.booklists[selected_booklist_name]
        self.selected_booklist = selected_booklist
        self.repopulate_books()

        if selected_booklist.is_user_created:
            self.button_new_book.configure(text="Add Book(s)")
            self.button_delete_book.configure(text="Remove Book(s)")
        else:
            self.button_new_book.configure(text="New Book", command=self.button_new_book_clicked)
            self.button_delete_book.configure(text="Delete Book", command=self.button_delete_book_clicked)

    def repopulate_bookslists(self):
        booklists: list[str] = []

        booklists.append("All Books")
        for booklist in self.bookshelf.booklists.values():
            if not booklist.is_user_created:
                continue
            booklists.append(booklist.name)

        self.scrollable_listbox_booklists.populate_items(booklists)

    def repopulate_books(self):
        texts: list[str] = []
        values: list[list[str]] = []
        for book_id in self.selected_booklist.books:
            book = self.bookshelf.books[book_id]
            texts.append(book.id)

            book_values = [book.title, book.author, book.publication_year] + [*book.custom_properties.values()]
            values.append(book_values)

        self.scrollable_treeview_books.populate_items(texts, values)
    
    def reconfigure_treeview_columns(self, columns: list[str]):
        self.scrollable_treeview_books.configure_columns(columns)

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

    def get_selected_book_id(self, message: str) -> int:
        selected_items = self.treeview_books.selection()
        if not selected_items:
            msgbox.showerror("Select a Book", "Please select a book to " + message + ".")
            return -1
        
        selected_item = selected_items[0]
        return int(self.treeview_books.item(selected_item)["text"])
    
    def button_new_booklist_clicked(self):
        name_window = NameBooklistWindow(self.root)
        self.root.wait_window(name_window)

        if name_window.confirmed:
            try:
                self.bookshelf.new_booklist(name_window.new_name)
            except ValueError:
                msgbox.showerror("Unable to Create Booklist", f"The booklist \"{name_window.new_name}\" already exists.")

        self.repopulate_bookslists()

    def button_rename_booklist_clicked(self):
        if not self.selected_booklist.is_user_created:
            msgbox.showerror("Cannot Rename Booklist", "You cannot rename this booklist.")
            return

        selected_booklist_name = self.selected_booklist.name
        
        rename_window = NameBooklistWindow(self.root, selected_booklist_name)
        self.root.wait_window(rename_window)

        if rename_window.confirmed:
            try:
                self.bookshelf.rename_booklist(selected_booklist_name, rename_window.new_name)
            except ValueError:
                msgbox.showerror("Unable to Rename Booklist", f"The booklist \"{rename_window.new_name}\" already exists.")

        self.repopulate_bookslists()

    def button_delete_booklist_clicked(self):
        booklist = self.selected_booklist
        if not booklist.is_user_created:
            msgbox.showerror("Cannot Delete Booklist", "You cannot delete this booklist.")
            return
        
        result = msgbox.askyesno("Delete Booklist", f"Are you sure you want to delete \"{booklist.name}\"?")

        if result:
            self.bookshelf.delete_booklist(booklist)

        self.repopulate_bookslists()

    def button_new_book_clicked(self):
        book = Book("", "", 0, self.bookshelf.custom_properties)

        edit_book_window = EditBookWindow(self.root, book, self.bookshelf)
        self.root.wait_window(edit_book_window)

        if edit_book_window.confirmed:
            selected_booklists: list[str] = []
            for name, value in edit_book_window.checkbutton_booklist_dict.items():
                if value.get() == 1:
                    selected_booklists.append(name)

            self.bookshelf.add_book(edit_book_window.book, selected_booklists)

        self.repopulate_books()

    def button_edit_book_clicked(self):
        selected_book_id = self.get_selected_book_id("edit")
        if selected_book_id == -1:
            return
        
        book = copy.deepcopy(self.bookshelf.books[selected_book_id])
        
        edit_book_window = EditBookWindow(self.root, book, self.bookshelf)
        self.root.wait_window(edit_book_window)

        if edit_book_window.confirmed:
            selected_booklists: list[str] = []
            for name, value in edit_book_window.checkbutton_booklist_dict.items():
                if value.get() == 1:
                    selected_booklists.append(name)

            self.bookshelf.update_book(edit_book_window.book, selected_booklists)

        self.repopulate_books()

    def button_delete_book_clicked(self):
        selected_book_id = self.get_selected_book_id("delete")
        if selected_book_id == -1:
            return
        
        selected_book = self.bookshelf.books[selected_book_id]
        
        result = msgbox.askyesno("Delete Book", "Are you sure you wish to pernamently delete \"" + selected_book.title + "\"?")

        if result:
            self.bookshelf.delete_book(selected_book)

        self.repopulate_books()
