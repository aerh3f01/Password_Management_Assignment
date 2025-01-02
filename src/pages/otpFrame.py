import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pyotp
import qrcode
import os

class OTPApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TOTP QR Code Generator")
        self.geometry("400x500")
        
        # Secret key storage
        self.secret_key = None
        
        # Username input
        self.label_username = ttk.Label(self, text="Enter Username:")
        self.label_username.pack(pady=10)
        
        self.entry_username = ttk.Entry(self)
        self.entry_username.pack(pady=5)
        
        # Generate QR Code button
        self.button_generate = ttk.Button(self, text="Generate QR Code", command=self.generate_qr_code)
        self.button_generate.pack(pady=10)
        
        # QR Code display
        self.qr_label = ttk.Label(self, text="Scan this QR code:")
        self.qr_label.pack(pady=5)
        
        self.qr_image_label = tk.Label(self)
        self.qr_image_label.pack(pady=10)
        
        # OTP display
        self.otp_label = ttk.Label(self, text="Your OTP will appear here after scanning.", font=("Helvetica", 12))
        self.otp_label.pack(pady=10)
    
    def generate_qr_code(self):
        username = self.entry_username.get().strip()
        
        if not username:
            self.otp_label.config(text="Please enter a username!", foreground="red")
            return
        
        # Generate a new secret key if not already done
        if not self.secret_key:
            self.secret_key = pyotp.random_base32()
        
        # Create a TOTP object
        totp = pyotp.TOTP(self.secret_key)
        
        # Create a URL for the QR code (compatible with most authenticator apps)
        otp_uri = totp.provisioning_uri(name=username, issuer_name="PassManApp")
        
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

if __name__ == "__main__":
    app = OTPApp()
    app.mainloop()
