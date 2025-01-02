import tkinter as tk
from tkinter import ttk
from pages import startFrame, loginFrame, registerFrame, passwordFrame

class PassManApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = ("Helvetica", 18)
        self.title("PassMan")

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (startFrame.StartPage, loginFrame.LoginPage, registerFrame.RegisterPage, passwordFrame.PasswordsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = PassManApp()
    app.mainloop()