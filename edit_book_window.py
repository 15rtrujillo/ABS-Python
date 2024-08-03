from book import Book
from bookshelf import Bookshelf
from scrollable_frame import ScrollableFrame


import tkinter as tk


class EditBookWindow(tk.Toplevel):
    def __init__(self, main_window: tk.Tk, book: Book, bookshelf: Bookshelf):
        super().__init__(main_window)
        self.book: Book = book
        self.bookshelf = bookshelf
        self.confirmed = False
        
        if not book.title:
            self.title("New Book")
        else:
            self.title("Edit Book")

        self.grab_set()

        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=40)
        self.rowconfigure(2, weight=5)
        self.rowconfigure(3, weight=40)
        self.rowconfigure(4, weight=10)
        self.columnconfigure(0, weight=1)

        self.label_instructions = tk.Label(self, text="Please specify the following information:")
        self.label_instructions.grid(row=0, column=0, sticky="ew")

        self.scrollable_properties = ScrollableFrame(self)
        self.scrollable_properties.grid(row=1, column=0, sticky="ew")

        self.frame_properties = self.scrollable_properties.inner_frame

        # Create properties
        self.entry_properties_dict: dict[str, tk.Entry] = {}
        self.__populate_properties()

        self.label_booklists = tk.Label(self, text="Please select which booklists this book should belong to.")
        self.label_booklists.grid(row=2, column=0, sticky="ew", padx=5)

        self.scrollable_booklists = ScrollableFrame(self)
        self.scrollable_booklists.grid(row=3, column=0, sticky="ew")

        self.frame_booklists = self.scrollable_booklists.inner_frame

        self.checkbutton_booklist_dict: dict[str, tk.IntVar] = {}
        self.__populate_booklists()

        # Buttons
        self.frame_buttons = tk.Frame(self)
        self.frame_buttons.grid(row=4, column=0)

        self.frame_buttons.rowconfigure(0, weight=1)
        self.frame_buttons.columnconfigure(0, weight=1)
        self.frame_buttons.columnconfigure(1, weight=1)

        self.button_confirm = tk.Button(self.frame_buttons, text="Confirm", command=self.button_confirm_clicked)
        self.button_confirm.grid(row=0, column=0, sticky="ew", padx=5)

        self.bind("<Return>", lambda _: self.button_confirm_clicked())

        self.button_cancel = tk.Button(self.frame_buttons, text="Cancel", command=self.destroy)
        self.button_cancel.grid(row=0, column=1, sticky="ew", padx=5)

    def __populate_properties(self):
        properties = ["Title", "Author", "Publication Year"] + [*self.book.custom_properties]
        for i in range(len(properties)):
            property = properties[i]

            label = tk.Label(self.frame_properties, text=property + ":")            
            label.grid(row=i, column=0, sticky="e", padx=5)

            entry = tk.Entry(self.frame_properties)
            entry.grid(row=i, column=1, sticky="ew")

            self.entry_properties_dict[property] = entry

            if self.book.title:
                if property == "Title":
                    entry.insert(0, self.book.title)
                elif property == "Author":
                    entry.insert(0, self.book.author)
                elif property == "Publication Year":
                    entry.insert(0, self.book.publication_year)
                else:
                    entry.insert(0, self.book.custom_properties[property])

    def __populate_booklists(self):
        i = 0
        for booklist in self.bookshelf.booklists.values():
            if not booklist.is_user_created:
                continue

            if self.book.id in booklist.books:
                selected = tk.IntVar(self, 1)
            else:
                selected = tk.IntVar(self, 0)

            checkbutton = tk.Checkbutton(self.frame_booklists, text=booklist.name, variable=selected)
            checkbutton.grid(row=i, column=0, sticky="w")
            i += 1

            self.checkbutton_booklist_dict[booklist.name] = selected
                    
    def button_confirm_clicked(self):
        self.confirmed = True

        self.book.title = self.entry_properties_dict["Title"].get()
        self.book.author = self.entry_properties_dict["Author"].get()
        self.book.publication_year = self.entry_properties_dict["Publication Year"].get()
        for property in self.book.custom_properties.keys():
            self.book.custom_properties[property] = self.entry_properties_dict[property].get()

        self.destroy()


if __name__ == "__main__":
    my_book = Book("My Princess", "Ryan", 1995, "Price", "Location")
    root = tk.Tk()
    root.bind("<Visibility>", lambda _: EditBookWindow(root, my_book, None))
    tk.mainloop()
