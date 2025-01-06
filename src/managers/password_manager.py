import keyring
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from managers.validation_manager import PasswordValidator

APP_NAME = "pass_man"

class PasswordManager:
    """
    Handles secure storage and management of passwords.

    This class provides functionalities to:
    - Encrypt and decrypt passwords.
    - Store passwords securely in a keyring.
    - Check for existing usernames.
    """

    def __init__(self):
        """
        Initializes the PasswordManager.
        """
        self._key = get_random_bytes(16)  # AES-128 key size

    def _encrypt(self, password):
        """Encrypts the given password using AES."""
        cipher = AES.new(self._key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(password.encode(), AES.block_size))
        return cipher.iv + ciphertext

    def _decrypt(self, encrypted_data):
        """Decrypts the given encrypted password using AES."""
        iv = encrypted_data[:AES.block_size]
        ciphertext = encrypted_data[AES.block_size:]
        cipher = AES.new(self._key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

    def _username_exists(self, username):
        """Checks if the username already exists in the keyring."""
        try:
            passwords = keyring.get_password(APP_NAME, username)
            return passwords is not None
        except keyring.errors.KeyringError as e:
            raise IOError(f"Keyring error while checking username: {e}")

    def load_passwords(self, username):
        """Loads the stored passwords for a user from the keyring."""
        try:
            encrypted_data = keyring.get_password(APP_NAME, username)
            if not encrypted_data:
                return {}
            passwords = self._decrypt(bytes.fromhex(encrypted_data))
            return eval(passwords)  # Convert string representation back to a dictionary
        except keyring.errors.KeyringError as e:
            raise IOError(f"Keyring error while loading passwords: {e}")

    def get_passwords(self, username):
        """Returns the stored passwords for the given username."""
        return self.load_passwords(username)

    def store_password(self, username, site, password):
        """Stores the password securely in the keyring."""
        try:
            validity = PasswordValidator.validate(password)
            if not validity:
                raise ValueError("Password is too weak.")

            # Load existing passwords or initialize an empty dictionary
            passwords = self.load_passwords(username)

            # Add the new password
            passwords[site] = password

            # Encrypt and save the updated passwords
            encrypted_passwords = self._encrypt(str(passwords)).hex()
            keyring.set_password(APP_NAME, username, encrypted_passwords)
        except keyring.errors.KeyringError as e:
            raise IOError(f"Keyring error while storing password: {e}")
        except ValueError as e:
            raise ValueError(f"Error storing the password: {e}")

    def delete_password(self, username, site):
        """Deletes the password associated with the given site for a user."""
        try:
            passwords = self.load_passwords(username)
            if site in passwords:
                del passwords[site]

                # Encrypt and save the updated passwords
                encrypted_passwords = self._encrypt(str(passwords)).hex()
                keyring.set_password(APP_NAME, username, encrypted_passwords)
            else:
                raise ValueError(f"No password found for site: {site}")
        except keyring.errors.KeyringError as e:
            raise IOError(f"Keyring error while deleting password: {e}")

    def add_password(self, username, site, password):
        """Adds a new password to the keyring."""
        try:
            passwords = self.load_passwords(username)
            if site in passwords:
                raise ValueError("Site already exists. Use a different site name or update the existing password.")

            self.store_password(username, site, password)
        except Exception as e:
            raise e
