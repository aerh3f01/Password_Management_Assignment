import pyotp
import time
import qrcode

totp = pyotp.TOTP('base32secret')


qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
mfa = pyotp.totp.TOTP('base32secret').provisioning_uri('Test_Name', issuer_name='Secure App')

qr.add_data(mfa)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("mfa.png")