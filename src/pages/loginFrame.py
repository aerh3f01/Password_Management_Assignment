# A simple login frame for the application
import tkinter as tk
from tkinter import ttk
from managers.login_manager import LoginManager, PasswordManagerError

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.login_manager = LoginManager()

        label = ttk.Label(self, text="Login", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.username_entry_label = ttk.Label(self, text="Enter username:")
        self.username_entry_label.pack()
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack()
        
        self.password_entry_label = ttk.Label(self, text="Enter password:")
        self.password_entry_label.pack()
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack()
        

        # OTP input
        self.otp_entry = ttk.Entry(self)
        self.otp_entry_label = ttk.Label(self, text="Enter OTP:")
        self.otp_entry_label.pack()
        self.otp_entry.pack()

        login_button = ttk.Button(self, text="Login", command=self.login)
        login_button.pack()

        back_button = ttk.Button(self, text="Back",
                                command=lambda: controller.show_frame("StartPage"))
        back_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        otp = self.otp_entry.get()
        try:
            self.login_manager.login(username, password)
            self.login_manager.verify_otp(otp)
            self.controller.show_frame("PasswordsPage")  # Navigate on success
        except PasswordManagerError as e:
            self.controller.handle_error(e)  # Display a known error
        except Exception as e:
            self.controller.handle_error(e)