from book import Book


import tkinter as tk
import tkinter.ttk as ttk


class EditBookWindow(tk.Toplevel):
    def __init__(self, main_window: tk.Tk, book: Book):
        super().__init__(main_window)
        self.book: Book = book
        self.confirmed = False
        
        if not book.title:
            self.title("New Book")
        else:
            self.title("Edit Book")

        self.grab_set()

        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=75)
        self.rowconfigure(2, weight=10)
        self.columnconfigure(0, weight=1)

        self.label_instructions = tk.Label(self, text="Please specify the following information:")
        self.label_instructions.grid(row=0, column=0, sticky="ew")

        self.frame_canvas = tk.Frame(self)
        self.frame_canvas.grid(row=1, column=0, sticky="nsew")

        self.frame_canvas.rowconfigure(0, weight=1)
        self.frame_canvas.columnconfigure(0, weight=98)
        self.frame_canvas.columnconfigure(1, weight=2)

        self.canvas_properties = tk.Canvas(self.frame_canvas)
        self.vscroll_properties = ttk.Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas_properties.yview)
        self.frame_properties = tk.Frame(self.canvas_properties)

        self.frame_properties.bind(
            "<Configure>",
            lambda e: self.canvas_properties.configure(
                scrollregion=self.canvas_properties.bbox("all")
            )
        )

        self.canvas_properties.create_window((0, 0), window=self.frame_properties, anchor="nw")

        self.canvas_properties.configure(yscrollcommand=self.vscroll_properties.set)

        self.canvas_properties.grid(row=0, column=0, sticky="nsew")
        self.vscroll_properties.grid(row=0, column=1, sticky="ns")

        # Create properties
        self.entry_properties_dict: dict[str, tk.Entry] = {}
        self.populate_form()

        self.frame_buttons = tk.Frame(self)
        self.frame_buttons.grid(row=2, column=0)

        self.frame_buttons.rowconfigure(0, weight=1)
        self.frame_buttons.columnconfigure(0, weight=1)
        self.frame_buttons.columnconfigure(1, weight=1)

        self.button_confirm = tk.Button(self.frame_buttons, text="Confirm", command=self.confirm)
        self.button_confirm.grid(row=0, column=0, sticky="ew", padx=5)

        self.button_cancel = tk.Button(self.frame_buttons, text="Cancel", command=self.destroy)
        self.button_cancel.grid(row=0, column=1, sticky="ew", padx=5)

    def populate_form(self):
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
                    
    def confirm(self):
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
    root.bind("<Visibility>", lambda e: EditBookWindow(root, my_book))
    tk.mainloop()
