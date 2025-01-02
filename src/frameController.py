import tkinter as tk
from tkinter import ttk
from pages import startFrame, loginFrame, registerFrame, passwordFrame
import traceback

class PassManApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = ("Helvetica", 18)
        self.title("PassMan")

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Create error message label
        self.error_label = ttk.Label(self, text="", foreground="red", wraplength=400)
        self.error_label.pack()

        self.frames = {}
        for F in (startFrame.StartPage, loginFrame.LoginPage, registerFrame.RegisterPage, passwordFrame.PasswordsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
    
    def set_error_message(self, message):
        """Display error messages on the GUI."""
        self.error_label.config(text=message)

    def clear_error_message(self):
        """Clear the error message from the GUI."""
        self.error_label.config(text="")

    def handle_error(self, exception):
        """Handle exceptions by updating the GUI and logging."""
        error_message = f"An error occurred: {exception}"
        traceback.print_exc() 
        self.set_error_message(error_message)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = PassManApp()
    app.mainloop()