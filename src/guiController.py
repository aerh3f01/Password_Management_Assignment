import tkinter as tk
from tkinter import ttk, messagebox
from managers import PasswordManager, PasswordValidator, PasswordGeneration, PassphraseGenerator


class PasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("700x500")
        
        # Default Styles
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 12))
        self.style.configure('TEntry', font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 12))
        
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
        self.username_label.grid(row=0, column=0, sticky=tk.W, pady=10)
        self.username_entry = ttk.Entry(self.main_frame)
        self.username_entry.grid(row=0, column=1, sticky=tk.W, pady=10)

        # Password
        self.password_label = ttk.Label(self.main_frame, text="Password:")
        self.password_label.grid(row=1, column=0, sticky=tk.W, pady=10)
        self.password_entry = ttk.Entry(self.main_frame, show="*")
        self.password_entry.grid(row=1, column=1, sticky=tk.W, pady=10)

        # Generate Password Button
        self.generate_button = ttk.Button(self.main_frame, text="Generate Password", command=self.generate_password)
        self.generate_button.grid(row=2, column=1, sticky=tk.W, pady=10)

        # Generate Passphrase Button
        self.generate_passphrase_button = ttk.Button(self.main_frame, text="Generate Passphrase", command=self.generate_passphrase)
        self.generate_passphrase_button.grid(row=3, column=1, sticky=tk.W, pady=10)

        # Copy Password Button
        self.copy_button = ttk.Button(self.main_frame, text="Copy Password", command=self.copy_password)
        self.copy_button.grid(row=2, column=2, sticky=tk.W, padx=10, pady=10)
        self.copy_button.state(["disabled"])  # Initially disabled

        # Store Password Button
        self.store_button = ttk.Button(self.main_frame, text="Store Password", command=self.store_password)
        self.store_button.grid(row=4, column=1, sticky=tk.W, pady=10)

        # Status
        self.status_label = ttk.Label(self.main_frame, text="", foreground="blue")
        self.status_label.grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=10)

        # Scrollable Suggestions Box
        self.scrollable_frame = ttk.Frame(self.main_frame)
        self.scrollable_frame.grid(row=6, column=0, columnspan=3, sticky=tk.W, pady=10)

        self.suggestions_text = tk.Text(self.scrollable_frame, wrap=tk.WORD, height=5, font=('Arial', 12), state='disabled')
        self.suggestions_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.scrollable_frame, orient=tk.VERTICAL, command=self.suggestions_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.suggestions_text.configure(yscrollcommand=self.scrollbar.set)



    def toggle_high_contrast(self):
        """Enable or disable high contrast mode."""
        self.high_contrast_mode = not self.high_contrast_mode
        if self.high_contrast_mode:
            # Apply high contrast styling
            self.style.configure('TLabel', background='black', foreground='white')
            self.style.configure('TEntry', fieldbackground='black', foreground='white')
            self.style.configure('TButton', background='black', foreground='white')

            # Update window and menu bar background
            self.root.config(bg='black')
            self.update_menu_styles(bg='black', fg='white', activebg='gray', activefg='white')
        else:
            # Revert to default styling
            self.style.configure('TLabel', background='light grey', foreground='black')
            self.style.configure('TEntry', fieldbackground='grey', foreground='black')
            self.style.configure('TButton', background='grey', foreground='black')

            # Update window and menu bar background to defaults
            self.root.config(bg='SystemButtonFace')
            self.update_menu_styles(bg='SystemButtonFace', fg='black', activebg='SystemHighlight', activefg='black')

    def update_menu_styles(self, bg, fg, activebg, activefg):
        """Helper function to update menu bar styles."""
        # Recreate the menu bar with updated styles
        self.menu_bar = tk.Menu(self.root, bg=bg, fg=fg, activebackground=activebg, activeforeground=activefg)
        self.root.config(menu=self.menu_bar)
        self.create_menu()



    def toggle_large_font(self):
        """Enable or disable large font mode."""
        self.large_font_mode = not self.large_font_mode
        font_size = 16 if self.large_font_mode else 12
        self.style.configure('TLabel', font=('Arial', font_size))
        self.style.configure('TEntry', font=('Arial', font_size))
        self.style.configure('TButton', font=('Arial', font_size))

    def generate_password(self):
        """Generate a strong password and display it."""
        password = self.password_generator.generate_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.status_label.config(text=f"Generated: {password} Keep it safe.", foreground="blue")
        self.copy_button.state(["!disabled"]) 

    def generate_passphrase(self):
        """Generate a passphrase and display it."""
        passphrase = PassphraseGenerator().generate_passphrase()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, passphrase)
        self.status_label.config(text=f"Generated: {passphrase} Keep it safe.", foreground="blue")
        self.copy_button.state(["!disabled"])

    def copy_password(self):
        """Copy the generated password to the clipboard."""
        password = self.password_entry.get().strip()
        if password:
            self.root.clipboard_clear()  # Clear the clipboard
            self.root.clipboard_append(password)  # Append the password
            self.root.update()  # Make sure the clipboard content is updated
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

        # Clear and update the suggestions box
        self.suggestions_text.configure(state='normal')  # Make text editable for updating
        self.suggestions_text.delete('1.0', tk.END)  # Clear previous suggestions
        if isinstance(suggestions, (list, tuple)):
            for suggestion in suggestions:
                self.suggestions_text.insert(tk.END, f"- {suggestion}\n")
        else:
            self.suggestions_text.insert(tk.END, suggestions)
        self.suggestions_text.configure(state='disabled')  # Make text read-only again

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
