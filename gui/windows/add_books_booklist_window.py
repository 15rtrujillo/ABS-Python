from model.book import Book
from gui.widgets.scrollable_treeview import ScrollableTreeview
from gui.widgets.search import Search


import tkinter as tk
import tkinter.messagebox as msgbox


class AddBooksBooklistWindow(tk.Toplevel):
    def __init__(self, master: tk.Tk, booklist_name: str, books: list[Book], default_properties: list[str]):
        super().__init__(master)

        self.booklist_name = booklist_name
        self.books = books
        self.search_results = books
        self.books_to_add: list[int] = []
        self.confirmed = False

        self.title("Add Books")
        self.geometry("800x350")

        self.focus_set()
        self.grab_set()

        self.rowconfigure(0, weight=10)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=70)
        self.rowconfigure(3, weight=10)
        self.columnconfigure(0, weight=1)

        self.label_instructions = tk.Label(self, text=f"Select the books you would like to add to \"{self.booklist_name}\".\nHint: You can hold \"Ctrl\" while clicking to select multiple books at once.")
        self.label_instructions.grid(row=0, column=0, sticky="ew")

        self.search = Search(self, default_properties)
        self.search.button_search.configure(command=self.button_search_clicked)
        self.search.grid(row=1, column=0)

        self.scrollable_treeview = ScrollableTreeview(self)
        self.scrollable_treeview.grid(row=2, column=0)

        self.frame_buttons = tk.Frame(self)
        self.frame_buttons.grid(row=3, column=0)

        self.frame_buttons.rowconfigure(0, weight=1)

        self.button_confirm = tk.Button(self.frame_buttons, text="Confirm", command=self.button_confirm_clicked)
        self.button_confirm.grid(row=0, column=0, sticky="e", padx=5)

        self.button_cancel = tk.Button(self.frame_buttons, text="Cancel", command=self.destroy)
        self.button_cancel.grid(row=0, column=1, sticky="w", padx=5)

        properties = self.search.default_options + [*self.books[0].custom_properties]
        self.search.configure_filters(properties)
        self.scrollable_treeview.configure_columns(properties)
        self.repopulate_books()

    def repopulate_books(self):
        books: dict[str, list[str]] = {}

        for book in self.search_results:
            book_values: list[str] = []

            default_properties = [property.lower().replace(" ", "_") for property in self.search.default_options]

            for property in default_properties:
                book_values.append(book.__dict__[property])
            book_values += [*book.custom_properties.values()]
            books[str(book.id)] = book_values

        self.scrollable_treeview.populate_items(books)

    def button_search_clicked(self):
        # If the search bar is empty, just reload the current booklist
        if not self.search.entry_search.get():
            self.search_results = self.books
            self.repopulate_books()
            return
        
        try:
            self.search_results = self.search.filter_books(self.books)
            self.repopulate_books()
        except Exception as e:
            msgbox.showerror("Error Searching", "There was an error while searching. Please report this bug.\n" + repr(e))

    def button_confirm_clicked(self):
        selected_items = self.scrollable_treeview.get_multiple_selection_text()

        if not selected_items:
            msgbox.showinfo("Select Books", f"You must select one or more books to add to the booklist \"{self.booklist_name}\".")
            return
        
        for item in selected_items:
            try:
                book_id = int(item)
                self.books_to_add.append(book_id)
            except ValueError:
                msgbox.showerror("Cannot Get Book ID", f"Cannot get the ID for treeview item {item}. Please report this bug.")

        self.confirmed = True
        self.destroy()
