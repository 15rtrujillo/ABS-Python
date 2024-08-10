# Release
# from gui.widgets.scrollable_listbox import ScrollableListbox
# Testing
from widgets.scrollable_listbox import ScrollableListbox


import tkinter as tk


class PropertiesWindow(tk.Toplevel):
    def __init__(self, master: tk.Tk, custom_properties: list[str]):
        super().__init__(master)

        self.title("Configure Book Properties")

        instructions = """You can add or remove properties for your books.
Properties allow you to better organize your books; you can search for and sort by the property values.
Adding a new property will default to a blank value for each book unless otherwise specified.
Removing a property will remove the value for ALL books and cannot be undone."""

        self.label_instructions = tk.Label(self, text=instructions)
        self.label_instructions.grid(row=0, column=0, padx=5)

        self.scrollable_listbox = ScrollableListbox(self)
        self.scrollable_listbox.grid(row=1, column=0, sticky="nsew", padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    window = PropertiesWindow(root, [])
    root.mainloop()
