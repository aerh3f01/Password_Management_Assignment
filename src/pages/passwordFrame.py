# The frame to manage passwords

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from managers.password_manager import PasswordManager
from managers.login_manager import LoginManager

class PasswordsPage(tk.Frame):
    """
    Manages the passwords page

    Parameters:
    username (str): The username of the user
    password (str): The password of the user

    Allows the user to view, add, and delete passwords

    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.password_manager = PasswordManager()
        self.login_manager = LoginManager()

        label = ttk.Label(self, text="Passwords", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.password_list = ttk.Treeview(self)
        self.password_list["columns"] = ("Website", "Username", "Password")
        self.password_list.column("#0", width=0, stretch=tk.NO)
        self.password_list.column("Website", anchor=tk.W, width=100)
        self.password_list.column("Username", anchor=tk.W, width=100)
        self.password_list.column("Password", anchor=tk.W, width=100)
        self.password_list.heading("#0", text="", anchor=tk.W)
        self.password_list.heading("Website", text="Website", anchor=tk.W)
        self.password_list.heading("Username", text="Username", anchor=tk.W)
        self.password_list.heading("Password", text="Password", anchor=tk.W)
        self.password_list.pack()

        self.update_password_list()

        add_button = ttk.Button(self, text="Add Password", command=self.add_password)
        add_button.pack()

        delete_button = ttk.Button(self, text="Delete Password", command=self.delete_password)
        delete_button.pack()

        back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        back_button.pack()

    def update_password_list(self):
        """
        Updates the password list with the current passwords
        """
        for password in self.password_manager.get_passwords():
            self.password_list.insert("", "end", text="", values=(password["website"], password["username"], password["password"]))

    def add_password(self):
        """
        Adds a new password to the list
        """
        website = simpledialog.askstring("Website", "Enter the website")
        username = simpledialog.askstring("Username", "Enter the username")
        password = simpledialog.askstring("Password", "Enter the password")
        self.password_manager.add_password(website, username, password)
        self.update_password_list()

    def delete_password(self):
        """
        Deletes a password from the list
        """
        selected = self.password_list.selection()
        if selected:
            item = self.password_list.item(selected)
            website = item["values"][0] # Website is the first value
            try:
                self.password_manager.delete_password(website)
                self.password_list.delete(selected)
            except Exception as e:
                self.controller.handle_error(e)
        else:
            tk.messagebox.showinfo("Error", "Please select a password to delete")



