import tkinter as tk


class AboutWindow(tk.Toplevel):
    def __init__(self, master: tk.Misc):
        super().__init__(master)

        self.title("About")

        self.focus_set()

        self.rowconfigure(0, weight=35)
        self.rowconfigure(1, weight=35)
        self.rowconfigure(2, weight=20)
        self.rowconfigure(3, weight=10)
        self.columnconfigure(0, weight=1)

        self.label_title = tk.Label(self, text="Aurora's Bookshelf", font=("Segoe UI", 18))
        self.label_title.grid(row=0, column=0)

        self.label_about = tk.Label(self, text="This program was created by Ryan for his princess, Aurora.")
        self.label_about.grid(row=1, column=0)

        self.label_version = tk.Label(self, text="v1.0.1")
        self.label_version.grid(row=2, column=0)

        self.button_close = tk.Button(self, text="Close", command=self.destroy)
        self.button_close.grid(row=3, column=0)

    
if __name__ == "__main__":
    window = tk.Tk()
    AboutWindow(window)
    window.mainloop()

