import tkinter as tk
import tkinter.ttk as ttk


class ScrollableListbox(tk.Frame):
    def __init__(self, master: tk.Misc):
        super().__init__(master)

        self.items: list[str] = []

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=98)
        self.columnconfigure(1, weight=2)

        self.listbox = tk.Listbox(self)
        self.listbox.grid(row=0, column=0, sticky="nsew")

        self.vscroll = ttk.Scrollbar(self)
        self.vscroll.config(command=self.listbox.yview)
        self.vscroll.grid(row=0, column=1, sticky="ns")

        self.listbox.configure(yscrollcommand=self.vscroll.set)

    def populate_items(self, items: list[str]):
        self.items = items

        self.listbox.delete(0, tk.END)

        for item in items:
            self.listbox.insert(tk.END, item)

    def update_item(self, old_item: str, new_item: str):
        try:
            index = self.items.index(old_item)
        except ValueError as e:
            raise ValueError(f"{old_item} does not exist in listbox.\n{repr(e)}")
        
        self.items[index] = new_item
        
        self.listbox.delete(index)
        self.listbox.insert(index, new_item)

    def get_selected_item(self) -> str | None:
        selected_items = self.listbox.curselection()

        if not selected_items:
            return None
        
        return self.listbox.get(selected_items[0])
