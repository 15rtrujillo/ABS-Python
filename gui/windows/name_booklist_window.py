import tkinter as tk
import tkinter.messagebox as msgbox


class NameBooklistWindow(tk.Toplevel):
    def __init__(self, master: tk.Misc, old_name: str | None = None):
        super().__init__(master)

        self.old_name = old_name
        self.new_name = ""
        self.confirmed = False

        self.grab_set()
        self.focus_set()

        self.rowconfigure(0, weight=33)
        self.rowconfigure(1, weight=33)
        self.rowconfigure(2, weight=33)
        self.columnconfigure(0, weight=1)

        self.label_instructions = tk.Label(self)
        self.label_instructions.grid(row=0, column=0, sticky="ew", padx=5)

        if self.old_name is None:
            self.title("New Booklist")
            self.label_instructions.configure(text="Please enter a name for the new booklist")
        else:
            self.title("Rename Booklist")
            self.label_instructions.configure(text="Please enter a new name for booklist currently titled \"" + self.old_name + "\"")

        self.entry_new_name = tk.Entry(self)
        self.entry_new_name.grid(row=1, column=0, sticky="ew", padx=5)

        self.frame_buttons = tk.Frame(self)
        self.frame_buttons.grid(row=2, column=0)

        self.frame_buttons.rowconfigure(0, weight=1)
        self.frame_buttons.columnconfigure(0, weight=50)
        self.frame_buttons.columnconfigure(1, weight=50)

        self.button_confirm = tk.Button(self.frame_buttons, text="Confirm", command=self.button_confirm_clicked)
        self.button_confirm.grid(row=0, column=0, sticky="ew", padx=5)

        self.button_cancel = tk.Button(self.frame_buttons, text="Cancel", command=self.destroy)
        self.button_cancel.grid(row=0, column=1, sticky="ew", padx=5)

        self.bind("<Return>", lambda _: self.button_confirm_clicked())

    def button_confirm_clicked(self):
        new_name = self.entry_new_name.get()
        if new_name == "":
            msgbox.showinfo("Enter a Name", "Please enter a name in the text box.")
            return
        
        self.confirmed = True
        self.new_name = new_name

        self.destroy()


if __name__ == "__main__":
    window = tk.Tk()
    NameBooklistWindow(window, "Wishlist")
    window.mainloop()
