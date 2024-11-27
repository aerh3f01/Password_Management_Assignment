import tkinter as tk
from tkinter import ttk, messagebox
from managers import PasswordManager, PasswordValidator, PasswordGeneration, PassphraseGenerator


class PasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("400x390")
        
        # Default Styles
        self.style = ttk.Style()
        self.high_contrast_mode = False
        self.large_font_mode = False
        
        self.validator = PasswordValidator()
        self.manager = PasswordManager()
        self.password_generator = PasswordGeneration()
        
        # Initialize menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.create_menu()
        
        # Frames
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Widgets
        self.create_widgets()

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

    def create_widgets(self):
        """Create and layout the main widgets."""
        # Username
        self.username_label = ttk.Label(self.main_frame, text="Username:")
        self.username_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_entry = ttk.Entry(self.main_frame)
        self.username_entry.grid(row=0, column=1, sticky=tk.W, pady=5)

        # Password
        self.password_label = ttk.Label(self.main_frame, text="Password:")
        self.password_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(self.main_frame, show="*")
        self.password_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

        # Generate Password Button
        self.generate_button = ttk.Button(self.main_frame, text="Generate Password", command=self.generate_password)
        self.generate_button.grid(row=2, column=0, sticky=tk.W, pady=5)

        # Generate Passphrase Button
        self.generate_passphrase_button = ttk.Button(self.main_frame, text="Generate Passphrase", command=self.generate_passphrase)
        self.generate_passphrase_button.grid(row=3, column=0, sticky=tk.W, pady=5)

        # Copy Password Button
        self.copy_button = ttk.Button(self.main_frame, text="Copy Password", command=self.copy_password)
        self.copy_button.grid(row=2, column=1, sticky=tk.W, pady=5)
        self.copy_button.state(["disabled"])  # Initially disabled

        # Store Password Button
        self.store_button = ttk.Button(self.main_frame, text="Store Password", command=self.store_password)
        self.store_button.grid(row=4, column=0, sticky=tk.W, pady=5)

        # Status Label
        self.status_label = ttk.Label(self.main_frame, text="", wraplength=300)
        self.status_label.grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=10)

        # Scrollable Suggestions Box
        self.scrollable_frame = ttk.Frame(self.main_frame)
        self.scrollable_frame.grid(row=6, column=0, columnspan=3, sticky=tk.W, pady=10)

        # Suggestion Label
        self.suggestions_label = ttk.Label(self.scrollable_frame, text="Password Suggestions:", font=('Arial', 10))
        self.suggestions_label.pack(side=tk.TOP, fill=tk.X)

        # Suggestions Text
        self.suggestions_text = tk.Text(
            self.scrollable_frame,
            wrap=tk.WORD,
            height=5,  # Control height
            width=38,  # Control width (smaller width here)
            font=('Arial', 12)
        )
        self.suggestions_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.scrollable_frame, orient=tk.VERTICAL, command=self.suggestions_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.suggestions_text.configure(yscrollcommand=self.scrollbar.set)

        # Set default suggestion text
        self.suggestions_text.insert(tk.END, "At least 8 characters\nAt least one uppercase letter\nAt least one number\nAt least one special character")
        self.suggestions_text.configure(state='disabled')

        # Set focus to the username entry
        self.username_entry.focus()

    def apply_default_styles(self):
        """Apply default styles for the app."""
        self.style.theme_use("default")
        self.style.configure("TLabel", background="SystemButtonFace", foreground="black")
        self.style.configure("TEntry", fieldbackground="white", foreground="black")
        self.style.configure("TButton", background="grey", foreground="black", padding=5)
        self.style.configure("TFrame", background="white")
        self.style.map("TButton", background=[("active", "light grey")])

        # Update the main frame background
        self.main_frame.config(style="TFrame")

        # Update Text widget styles
        self.suggestions_text.configure(background="white", foreground="black", insertbackground="black")  # Cursor color

        # Update the root background
        self.root.config(bg="SystemButtonFace")

    def apply_high_contrast_styles(self):
        """Apply high contrast styles for the app."""
        # Update ttk widget styles
        self.style.configure("TLabel", background="black", foreground="white")
        self.style.configure("TEntry", fieldbackground="black", foreground="white")
        self.style.configure("TButton", background="black", foreground="white", padding=5)
        self.style.configure("TFrame", background="black")
        self.style.map("TButton", background=[("active", "grey")])

        # Update the root background color
        self.root.config(bg="black")

        # Update the main frame background
        self.main_frame.config(style="TFrame")

        # Update Text widget styles
        self.suggestions_text.configure(background="black", foreground="white", insertbackground="white")  # Cursor color



    def toggle_high_contrast(self):
        """Enable or disable high contrast mode."""
        self.high_contrast_mode = not self.high_contrast_mode
        if self.high_contrast_mode:
            self.apply_high_contrast_styles()
        else:
            self.apply_default_styles()

    def toggle_large_font(self):
        """Enable or disable large font mode."""
        self.large_font_mode = not self.large_font_mode
        font_size = 16 if self.large_font_mode else 12
        self.style.configure('TLabel', font=('Arial', font_size))
        self.style.configure('TEntry', font=('Arial', font_size))
        self.style.configure('TButton', font=('Arial', font_size))

    def generate_password(self):
        """Generate a strong password and display it."""
        password = self.password_generator.generate_secure_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.status_label.config(text=f"Generated: {password} \nKeep it safe.", foreground="green")
        self.copy_button.state(["!disabled"])

    def generate_passphrase(self):
        """Generate a passphrase and display it."""
        passphrase = PassphraseGenerator().generate_passphrase()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, passphrase)
        self.status_label.config(text=f"Generated: {passphrase} \nKeep it safe.", foreground="orange")
        self.copy_button.state(["!disabled"])

    def copy_password(self):
        """Copy the generated password to the clipboard."""
        password = self.password_entry.get().strip()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.root.update()
            self.status_label.config(text="Password copied to clipboard!", foreground="green")
        else:
            self.status_label.config(text="No password to copy!", foreground="red")

    def store_password(self):
        """Store the entered username and password securely."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username:
            messagebox.showerror("Input Error", "Username cannot be empty.")
            return
        if not password:
            messagebox.showerror("Input Error", "Password cannot be empty.")
            return
        
        result = self.validator.validate(password)
        if isinstance(result, tuple):
            validation_result, suggestions = result
        else:
            validation_result, suggestions = result, "No password suggestions."

        self.suggestions_text.configure(state='normal')
        self.suggestions_text.delete('1.0', tk.END)
        if isinstance(suggestions, (list, tuple)):
            for suggestion in suggestions:
                self.suggestions_text.insert(tk.END, f"- {suggestion}\n")
        else:
            self.suggestions_text.insert(tk.END, suggestions)
        self.suggestions_text.configure(state='disabled')

        if validation_result == "strong":
            result = self.manager.store_password(username, password)
            self.status_label.config(text=result, foreground="green")
        elif validation_result == "weak":
            weak_msg = "Weak password. Would you like to proceed anyway?"
            if messagebox.askyesno("Weak Password", weak_msg):
                result = self.manager.store_password(username, password)
                self.status_label.config(text=result, foreground="orange")
            else:
                self.status_label.config(text="Weak password rejected.", foreground="red")
        else:
            self.status_label.config(text="Invalid password.", foreground="red")

    def show_about(self):
        """Display information about the application."""
        messagebox.showinfo("About", "Professional Password Manager v1.0\nSecurely store and manage your passwords.")

    def show_help(self):
        """Display help information."""
        messagebox.showinfo("Help", "1. Enter your username and password.\n"
                                    "2. Use 'Generate Password' for a secure password.\n"
                                    "3. Click 'Store Password' to save it.")


def main():
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
