import tkinter as tk
import tkinter.messagebox as msgbox


class NewPropertyWindow(tk.Toplevel):
    def __init__(self, master: tk.Misc):
        super().__init__(master)

        self.property_name = ""
        self.default_value = ""
        self.confirmed = False

        self.title("New Property")

        self.grab_set()
        self.focus_set()

        self.rowconfigure(0, weight=15)
        self.rowconfigure(1, weight=75)
        self.rowconfigure(2, weight=10)
        self.columnconfigure(0, weight=1)

        instructions = """Please enter the name (key) for the new property.
You can also specify a default value that will be applied to all books
(which you can still change later).
You may leave the default value blank."""

        self.instructions_label = tk.Label(self, text=instructions)
        self.instructions_label.grid(row=0, column=0, sticky="ew", padx=5)

        self.frame_contents = tk.Frame(self)
        self.frame_contents.grid(row=1, column=0, sticky="nsew")

        self.frame_contents.rowconfigure(0, weight=50)
        self.frame_contents.rowconfigure(1, weight=50)
        self.frame_contents.columnconfigure(0, weight=50)
        self.frame_contents.columnconfigure(1, weight=50)

        self.label_name = tk.Label(self.frame_contents, text="Property Name:")
        self.label_name.grid(row=0, column=0, sticky="e")

        self.label_default = tk.Label(self.frame_contents, text="Default Value")
        self.label_default.grid(row=1, column=0, sticky="e")

        self.entry_name = tk.Entry(self.frame_contents)
        self.entry_name.grid(row=0, column=1, sticky="ew", padx=5)

        self.entry_default = tk.Entry(self.frame_contents)
        self.entry_default.grid(row=1, column=1, sticky="ew", padx=5)

        self.frame_buttons = tk.Frame(self)
        self.frame_buttons.grid(row=2, column=0, sticky="nsew")

        self.frame_buttons.rowconfigure(0, weight=1)
        self.frame_buttons.columnconfigure(0, weight=50)
        self.frame_buttons.columnconfigure(1, weight=50)

        self.button_confirm = tk.Button(self.frame_buttons, text="Confirm", command=self.button_confirm_clicked)
        self.button_confirm.grid(row=0, column=0, sticky="e", padx=5)

        self.button_cancel = tk.Button(self.frame_buttons, text="Cancel", command=self.destroy)
        self.button_cancel.grid(row=0, column=1, sticky="w", padx=5)

        self.bind("<Return>", lambda _: self.button_confirm_clicked())

    def button_confirm_clicked(self):
        self.property_name = self.entry_name.get()
        if not self.property_name:
            msgbox.showinfo("Enter a Name", "Please enter a name for the new property.")
            return
        
        self.default_value = self.entry_default.get()
        self.confirmed = True

        self.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    window = NewPropertyWindow(root)
    root.mainloop()
