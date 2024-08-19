from gui.about_window import AboutWindow
from book import Book
from booklist import Booklist
from bookshelf import Bookshelf
from gui.add_books_booklist_window import AddBooksBooklistWindow
from gui.edit_book_window import EditBookWindow
from gui.name_booklist_window import NameBooklistWindow
from gui.properties_window import PropertiesWindow
from gui.widgets.scrollable_listbox import ScrollableListbox
from gui.widgets.scrollable_treeview import ScrollableTreeview
from gui.widgets.search import Search


import copy
import tkinter as tk
import tkinter.messagebox as msgbox
import tkinter.ttk as ttk


class ABS(tk.Tk):
    def __init__(self, bookshelf: Bookshelf):
        super().__init__()
        self.bookshelf = bookshelf
        self.selected_booklist: Booklist = bookshelf.booklists["All Books"]

        self.title("Aurora's Bookshelf")
        self.geometry("1200x600")

        self.__create_menu_bar()
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=22)
        self.columnconfigure(1, weight=5)
        self.columnconfigure(2, weight=73)

        self.__create_booklist_frame()

        # Vertical separator
        self.separator = ttk.Separator(self, orient="vertical")
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
        self.menu_bar = tk.Menu(self)

        # File menu
        self.menu_file = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_file.add_command(label="Open Bookshelf File Location", command=self.menu_open_file_location_clicked)
        self.menu_bar.add_cascade(label="File", menu=self.menu_file)

        # Edit menu
        self.menu_edit = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_edit.add_command(label="Edit Book Properties", command=self.menu_edit_book_properties_clicked)
        self.menu_bar.add_cascade(label="Edit", menu=self.menu_edit)

        # Help Menu
        self.menu_help = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_help.add_command(label="About", command=lambda: AboutWindow(self))
        self.menu_bar.add_cascade(label="Help", menu=self.menu_help)

        self.config(menu=self.menu_bar)

    def __create_booklist_frame(self):
        self.frame_booklists = tk.Frame(self)
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
        self.frame_books = tk.Frame(self)
        self.frame_books.grid(row=0, column=2, sticky="nsew")

        self.frame_books.rowconfigure(0, weight=10)
        self.frame_books.rowconfigure(1, weight=80)
        self.frame_books.rowconfigure(2, weight=10)
        self.frame_books.columnconfigure(0, weight=1)

        # Search frame
        self.search = Search(self.frame_books, self.bookshelf.built_in_properties)
        self.search.grid(row=0, column=0, sticky="nsew")
        self.search.button_search.configure(command=self.button_search_clicked)

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
        self.button_delete_book = tk.Button(self.frame_books_buttons, text="Delete Book(s)", command=self.button_delete_book_clicked)
        self.button_delete_book.grid(row=0, column=2, sticky="e", padx=5)

    def show_window(self):
        self.mainloop()

    def listbox_booklists_selection_changed(self):   
        selected_booklist_name = self.scrollable_listbox_booklists.get_selected_item()
        if selected_booklist_name is None:
            return
        
        selected_booklist = self.bookshelf.booklists[selected_booklist_name]
        self.selected_booklist = selected_booklist

        self.repopulate_books()

        if selected_booklist.is_user_created:
            self.button_new_book.configure(text="Add Book(s)", command=self.button_add_books_clicked)
            self.button_delete_book.configure(text="Remove Book(s)")
        else:
            self.button_new_book.configure(text="New Book", command=self.button_new_book_clicked)
            self.button_delete_book.configure(text="Delete Book(s)", command=self.button_delete_book_clicked)

    def repopulate_bookslists(self):
        self.scrollable_listbox_booklists.populate_items([*self.bookshelf.booklists])

    def repopulate_books(self):
        texts: list[str] = []
        values: list[list[str]] = []
        for book in self.selected_booklist.books:
            texts.append(book.id)

            book_values = [book.title, book.author, book.publication_year] + [*book.custom_properties.values()]
            values.append(book_values)

        self.scrollable_treeview_books.populate_items(texts, values)
    
    def reconfigure_treeview_columns(self, columns: list[str]):
        self.scrollable_treeview_books.configure_columns(columns)

    def reconfigure_filters(self, filters: list[str]):
        self.search.configure_filters(filters)

    def update_properties(self):
        all_properties = self.bookshelf.built_in_properties + self.bookshelf.custom_properties
        self.reconfigure_treeview_columns(all_properties)
        self.reconfigure_filters(all_properties)

    def menu_open_file_location_clicked(self):
        import file_utils
        import os
        if os.name == "nt":
            import subprocess
            subprocess.Popen(f"explorer {file_utils.get_data_directory()}")
        else:
            msgbox.showinfo("Windows Only", f"This feature is only available on Windows systems. You can manually naviagte to \"{file_utils.get_data_directory()}\" to find the Bookshelf files.")

    def menu_edit_book_properties_clicked(self):
        custom_properties = copy.deepcopy(self.bookshelf.custom_properties)

        window = PropertiesWindow(self, custom_properties, self.bookshelf.new_property, self.bookshelf.delete_property)
        self.wait_window(window)

        self.update_properties()
        self.repopulate_books()
    
    def button_new_booklist_clicked(self):
        name_window = NameBooklistWindow(self)
        self.wait_window(name_window)

        if name_window.confirmed:
            try:
                self.bookshelf.new_booklist(name_window.new_name)
                self.repopulate_bookslists()
            except ValueError:
                msgbox.showerror("Unable to Create Booklist", f"The booklist \"{name_window.new_name}\" already exists.")

    def button_rename_booklist_clicked(self):
        if not self.selected_booklist.is_user_created:
            msgbox.showerror("Cannot Rename Booklist", "You cannot rename this booklist.")
            return

        selected_booklist_name = self.selected_booklist.name
        
        rename_window = NameBooklistWindow(self, selected_booklist_name)
        self.wait_window(rename_window)

        if rename_window.confirmed:
            try:
                self.bookshelf.rename_booklist(selected_booklist_name, rename_window.new_name)
                self.repopulate_bookslists()
            except ValueError:
                msgbox.showerror("Unable to Rename Booklist", f"The booklist \"{rename_window.new_name}\" already exists.")

    def button_delete_booklist_clicked(self):
        booklist = self.selected_booklist
        if not booklist.is_user_created:
            msgbox.showerror("Cannot Delete Booklist", "You cannot delete this booklist.")
            return
        
        result = msgbox.askyesno("Delete Booklist", f"Are you sure you want to delete \"{booklist.name}\"?")

        if result:
            self.bookshelf.delete_booklist(booklist)
            self.repopulate_bookslists()

    def button_search_clicked(self):
        # If the search bar is empty, just reload the current booklist
        if not self.search.entry_search.get():
            self.repopulate_books()
            return

        current_booklist = self.selected_booklist

        try:
            found_books = self.search.filter_books(current_booklist.books)
        except Exception as e:
            msgbox.showerror("Error Searching", "There was an error while searching. Please report this bug.\n" + repr(e))

        temp_booklist = Booklist("search_results", False, found_books)
        self.selected_booklist = temp_booklist
        self.repopulate_books()
        self.selected_booklist = current_booklist

    def button_new_book_clicked(self):
        book = Book("", "", "", self.bookshelf.custom_properties)

        edit_book_window = EditBookWindow(self, book, self.bookshelf, True)
        self.wait_window(edit_book_window)

        if edit_book_window.confirmed:
            selected_booklists: list[str] = []
            for name, value in edit_book_window.checkbutton_booklist_dict.items():
                if value.get() == 1:
                    selected_booklists.append(name)

            self.bookshelf.add_book(edit_book_window.book, selected_booklists)
            self.repopulate_books()

    def button_add_books_clicked(self):
        # FINISHME
        books = [book for book in self.bookshelf.books.values() if book.id not in self.selected_booklist.books]
        window = AddBooksBooklistWindow(self, self.selected_booklist.name, books)

    def button_edit_book_clicked(self):
        selected_book = self.scrollable_treeview_books.get_selected_text()
        if selected_book is None:
            msgbox.showinfo("Please Select a Book", "Please select a book to edit.")
            return
        
        selected_book_id = int(selected_book)
        book = copy.deepcopy(self.bookshelf.books[selected_book_id])
        
        edit_book_window = EditBookWindow(self, book, self.bookshelf)
        self.wait_window(edit_book_window)

        if edit_book_window.confirmed:
            selected_booklists: list[str] = []
            for name, value in edit_book_window.checkbutton_booklist_dict.items():
                if value.get() == 1:
                    selected_booklists.append(name)

            self.bookshelf.update_book(edit_book_window.book, selected_booklists)
            self.repopulate_books()

    def button_delete_book_clicked(self):
        selected_books = self.scrollable_treeview_books.get_multiple_selection_text()
        if selected_books is None:
            msgbox.showinfo("Please Select a Book", "Please select a book to delete.\nHint: You can hold \"Ctrl\" while clicking to select multiple books at once.")
            return
        
        if len(selected_books) > 1:
            result = msgbox.askyesno("Delete Book", "Are you sure you wish to delete " + str(len(selected_books)) + " books?")
        elif len(selected_books) == 1:
            selected_book = self.bookshelf.books[int(selected_books[0])]
            result = msgbox.askyesno("Delete Book", "Are you sure you wish to pernamently delete \"" + selected_book.title + "\"?\nHint: You can hold \"Ctrl\" while clicking to select multiple books at once.")
        else:
            msgbox.showerror("No Books Selected", "Attempting to delete books with none selected. Please report this bug.")
            return

        if result:
            for text in selected_books:
                try:
                    selected_book_id = int(text)
                    selected_book = self.bookshelf.books[selected_book_id]
                    self.bookshelf.delete_book(selected_book)
                except:
                    msgbox.showerror("Int Conversion Failed", f"Error getting the selected book. \"text\" is \"{text}\". Please report this bug.")
            self.repopulate_books()
