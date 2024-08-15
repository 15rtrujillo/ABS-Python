import tkinter as tk
import tkinter.ttk as ttk


class ScrollableTreeview(tk.Frame):
    def __init__(self, master: tk.Misc):
        super().__init__(master)

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
        for column in columns:
            self.treeview.heading(column, text=column)
            self.treeview.column(column, width=150, stretch=True)

    def populate_items(self, texts: list[str], values: list[list[str]]):
        """Clears all itmes in the treeview and repopulates them"""
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        for i in range (len(texts)):
            self.treeview.insert("", "end",
                                 text=texts[i],
                                 values=values[i])
            
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
