# A simple login frame for the application
import tkinter as tk
from tkinter import ttk
from managers.login_manager import LoginManager
import keyring
import os


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.login_manager = LoginManager()

        label = ttk.Label(self, text="Login", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.username_entry = ttk.Entry(self)
        self.username_entry.pack()
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack()

        login_button = ttk.Button(self, text="Login", command=self.login)
        login_button.pack()

        back_button = ttk.Button(self, text="Back",
                                command=lambda: controller.show_frame("StartPage"))
        back_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            self.login_manager.login(username, password)
            self.controller.show_frame("PasswordsPage")
        except ValueError as e:
            error_label = ttk.Label(self, text=str(e))
            error_label.pack()

            
