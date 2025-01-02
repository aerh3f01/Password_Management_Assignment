## The main opening frame of the application
import tkinter as tk
from tkinter import ttk

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text="Welcome to PassMan", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = ttk.Button(self, text="Login",
                            command=lambda: controller.show_frame("LoginPage"))
        button2 = ttk.Button(self, text="Register",
                            command=lambda: controller.show_frame("RegisterPage"))
        button1.pack()
        button2.pack()

        