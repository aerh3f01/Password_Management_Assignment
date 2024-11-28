import tkinter as tk
from tkinter import ttk, messagebox
from managers import PasswordManager, PasswordValidator, PasswordGeneration, PassphraseGenerator

class PasswordManager(tk.Tk):

    def __init__(self):
        # Initial setups
        super().__init__()
        self.title("Password Manager")
        self.geometry("400x390")

        # Default Styles
        self.style = ttk.Style()
        self.high_contrast_mode = False
        self.large_font_mode = False
        
        # Initialise the external methods
        self.validator = PasswordValidator()
        self.manager = PasswordManager()
        self.password_generator = PasswordGeneration()
        self.passphrase_generator = PassphraseGenerator()

        # Create the basic screens
        self.login_frame = self.create_login_frame()
        self.register_frame = self.create_register_frame()
        self.data_management_frame = self.create_data_management_frame()

        self.login_frame.pack()

        # Apply default styles
        self.apply_default_styles()

    def create_menu(self):
        """Recreate the menu bar to reflect style changes."""
        # Accessibility Menu
        accessibility_menu = tk.Menu(self.menu_bar, tearoff=0, bg=self.menu_bar.cget('bg'), fg=self.menu_bar.cget('fg'))
        accessibility_menu.add_checkbutton(label="Enable High Contrast", command=self.toggle_high_contrast)
        accessibility_menu.add_checkbutton(label="Enable Large Fonts", command=self.toggle_large_font)
        self.menu_bar.add_cascade(label="Accessibility", menu=accessibility_menu)

        # Help Menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0, bg=self.menu_bar.cget('bg'), fg=self.menu_bar.cget('fg'))
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Help", command=self.show_help)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        # Login Menu
        logout_menu = tk.Menu(self.menu_bar, tearoff=0, bg=self.menu_bar.cget('bg'), fg=self.menu_bar.cget('fg'))
        logout_menu.add_command(label="Logout", command=self.logout)

        
    def create_login_frame(self):
        """
        Create the basic login screen for the application
        """
