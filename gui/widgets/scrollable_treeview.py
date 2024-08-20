import tkinter as tk
import tkinter.ttk as ttk


class ScrollableTreeview(tk.Frame):
    def __init__(self, master: tk.Misc):
        super().__init__(master)

        self.sort_by: int | None = None
        self.reverse_sort = False

        self.rowconfigure(0, weight=98)
        self.rowconfigure(1, weight=2)
        self.columnconfigure(0, weight=98)
        self.columnconfigure(1, weight=2)

        self.treeview = ttk.Treeview(self, show="headings")

        # Scrollbars
        self.hscroll = ttk.Scrollbar(self, orient="horizontal", command=self.treeview.xview)
        self.vscroll = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)

        self.treeview.configure(xscrollcommand=self.hscroll.set, yscrollcommand=self.vscroll.set)

        self.treeview.grid(row=0, column=0, sticky="nsew")
        self.vscroll.grid(row=0, column=1, sticky="ns")
        self.hscroll.grid(row=1, column=0, sticky="ew")

    def configure_columns(self, columns: list[str]):
        self.treeview.configure(columns=columns)
        for i in range(len(columns)):
            column = columns[i]
            self.treeview.heading(column, text=column, command=lambda i=i: self.column_heading_clicked(i))
            self.treeview.column(column, width=100, stretch=True)

    def populate_items(self, items: dict[str, list[str]]):
        """Clears all itmes in the treeview and repopulates them"""
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        if self.sort_by is not None:
            try:
                # I convert to a string here because entries that are pure integers get converted to ints.
                # That makes empty entries break the comparison, because they stay strings.
                sorted_items = dict(sorted(items.items(), key=lambda i: str(i[1][self.sort_by]), reverse=self.reverse_sort))
                items = sorted_items
            except Exception as e:
                print("Error sorting: " + repr(e))

        for text, values in items.items():
            self.treeview.insert("", "end",
                                 text=text,
                                 values=values)
            
    def get_multiple_selection_text(self) -> list[str] | None:
        selected_items = self.treeview.selection()
        if not selected_items:
            return None
        
        texts: list[str] = []
        for selected_item in selected_items:
            texts.append(self.treeview.item(selected_item)["text"])
        return texts

    def get_selected_text(self) -> str | None:
        selected_texts = self.get_multiple_selection_text()
        if selected_texts is None:
            return None
        
        return selected_texts[0]

    def column_heading_clicked(self, column: int):
        if column == self.sort_by:
            self.reverse_sort = not self.reverse_sort
        else:
            self.sort_by = column
            self.reverse_sort = False

        # Grab all the items already in the treeview.
        # We're creating a dictionary from the text: values
        # Where text is the book's id and values is a list of the properties
        items = {self.treeview.item(item)["text"]: self.treeview.item(item)["values"] for item in self.treeview.get_children()}
        self.populate_items(items)
