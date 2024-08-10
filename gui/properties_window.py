# Release
# from gui.widgets.scrollable_listbox import ScrollableListbox
# Testing
from widgets.scrollable_listbox import ScrollableListbox


import tkinter as tk
import tkinter.messagebox as msgbox


class PropertiesWindow(tk.Toplevel):
    def __init__(self, master: tk.Tk, custom_properties: list[str]):
        super().__init__(master)

        self.custom_properties = custom_properties
        self.change_made = False

        self.title("Configure Book Properties")

        self.grab_set()
        self.focus_set()

        self.rowconfigure(0, weight=15)
        self.rowconfigure(1, weight=5)
        self.rowconfigure(2, weight=60)
        self.rowconfigure(3, weight=10)
        self.rowconfigure(4, weight=10)
        self.columnconfigure(0, weight=1)

        instructions = """You can add or remove properties for your books.
Properties allow you to better organize your books; you can search for and sort by the property values.
Adding a new property will default to a blank value for each book unless otherwise specified.
Removing a property will remove the value for ALL books and cannot be undone."""

        self.label_instructions = tk.Label(self, text=instructions)
        self.label_instructions.grid(row=0, column=0, sticky="ew", padx=5)

        self.label_your_properties = tk.Label(self, text="Your Custom Properties")
        self.label_your_properties.grid(row=1, column=0, sticky="ew", padx=5)

        self.scrollable_listbox = ScrollableListbox(self)
        self.scrollable_listbox.grid(row=2, column=0, sticky="nsew", padx=5)
        self.scrollable_listbox.populate_items(custom_properties)

        self.frame_properties_buttons = tk.Frame(self)
        self.frame_properties_buttons.grid(row=3, column=0, sticky="nsew")

        self.frame_properties_buttons.rowconfigure(0, weight=1)
        self.frame_properties_buttons.columnconfigure(0, weight=50)
        self.frame_properties_buttons.columnconfigure(1, weight=50)

        self.button_new_property = tk.Button(self.frame_properties_buttons, text="New Property")
        self.button_new_property.grid(row=0, column=0, sticky="e", padx=5)

        self.button_delete_property = tk.Button(self.frame_properties_buttons, text="Delete Property", command=self.button_delete_property_clicked)
        self.button_delete_property.grid(row=0, column=1, sticky="w", padx=5)

        self.button_close = tk.Button(self, text="Close", command=self.destroy)
        self.button_close.grid(row=4, column=0)

    def button_delete_property_clicked(self):
        selection = self.scrollable_listbox.get_selected_item()

        if selection is None:
            msgbox.showinfo("Select a Property", "Please select a property from the list to delete.")
            return
        
        result = msgbox.askyesno("Delete Property",
                                 f"""Are you sure you want to delete the property \"{selection}\"?
This will remove the property from all books.
You CANNOT undo this action.""")
        
        if result:
            self.custom_properties.remove(selection)
            self.scrollable_listbox.populate_items(self.custom_properties)


if __name__ == "__main__":
    root = tk.Tk()
    window = PropertiesWindow(root, ["test guy1", "test guy2"])
    root.mainloop()
