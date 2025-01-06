# A page for registration of new users
import tkinter as tk
from tkinter import ttk
from managers.login_manager import LoginManager
import pyotp
import qrcode
from PIL import Image, ImageTk

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.login_manager = LoginManager()

        # Secret key storage
        self.secret_key = None

        label = ttk.Label(self, text="Register", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.username_entry = ttk.Entry(self)
        self.username_entry.pack()
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack()

        register_button = ttk.Button(self, text="Register", command=self.register)
        register_button.pack()

        # QR Code display
        self.qr_label = ttk.Label(self, text="Scan this QR code:")
        self.qr_label.pack(pady=5)

        self.qr_image_label = tk.Label(self)
        self.qr_image_label.pack(pady=10)

        # OTP display
        self.otp_label = ttk.Label(self, text="Your OTP will appear here after generating, scan to use an authentication app.", font=("Helvetica", 12))
        self.otp_label.pack(pady=10)

        # OTP Verification section
        self.otp_entry_label = ttk.Label(self, text="Enter OTP for verification:")
        self.otp_entry_label.pack(pady=5)

        self.otp_entry = ttk.Entry(self)
        self.otp_entry.pack()

        verify_otp_button = ttk.Button(self, text="Verify OTP", command=self.verify_otp)
        verify_otp_button.pack(pady=5)

        back_button = ttk.Button(self, text="Back",
                                command=lambda: controller.show_frame("StartPage"))
        back_button.pack()

        next_button = ttk.Button(self, text="Next",
                                command=lambda: controller.show_frame("LoginPage"))
        next_button.pack()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            self.login_manager.register(username, password)
            self.controller.set_error_message("Registration successful!")
            self.controller.shared_data["username"] = username
            self.controller.shared_data["userpin"] = self.login_manager.get_userpin(username)
            self.generate_qr_code()
        except Exception as e:
            self.controller.handle_error(e)

    def generate_qr_code(self):
        username = self.username_entry.get()

        if not username:
            self.otp_label.config(text="Please enter a username!", foreground="red")
            return

        # Generate a new secret key if not already done
        if not self.secret_key:
            self.secret_key = pyotp.random_base32()

        # Create a TOTP object
        totp = pyotp.TOTP(self.secret_key)

        # Create a URL for the QR code (compatible with most authenticator apps)
        otp_uri = totp.provisioning_uri(name=username, issuer_name="PassMan")

        # Generate QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(otp_uri)
        qr.make(fit=True)

        # Save the QR Code as an image
        qr_image_path = "otp_qr_code.png"
        qr_image = qr.make_image(fill="black", back_color="white")
        qr_image.save(qr_image_path)

        # Display the QR code in the application
        img = Image.open(qr_image_path)
        img = img.resize((200, 200), Image.LANCZOS)
        self.qr_image = ImageTk.PhotoImage(img)
        self.qr_image_label.config(image=self.qr_image)

        # Display OTP for testing (optional)
        self.update_otp()

    def update_otp(self):
        # Generate the current OTP
        if self.secret_key:
            totp = pyotp.TOTP(self.secret_key)
            otp = totp.now()
            self.otp_label.config(text=f"Current OTP: {otp}", foreground="green")
        else:
            self.otp_label.config(text="No secret key found. Generate QR code first.", foreground="red")

    def verify_otp(self):
        # Verify the entered OTP
        entered_otp = self.otp_entry.get()
        if self.secret_key:
            totp = pyotp.TOTP(self.secret_key)
            if totp.verify(entered_otp):
                self.otp_label.config(text="OTP Verified Successfully!", foreground="green")
            else:
                self.otp_label.config(text="Invalid OTP. Please try again.", foreground="red")
        else:
            self.otp_label.config(text="No secret key found. Generate QR code first.", foreground="red")