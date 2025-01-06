# A registration and login manager for the application

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import keyring
from managers.validation_manager import PasswordValidator
import pyotp

APP_NAME = "pass_man"

class PasswordManagerError(Exception):
    ## Blanket exception for PasswordManager
    ''' Helps mitigate module errors that dont accept specific exceptions '''
    pass

APP_NAME = "pass_man"

class LoginManager:
    """
    Handles user registration and login with secure password hashing and storage.
    """
    def __init__(self):
        self.ph = PasswordHasher()
        self.validator = PasswordValidator()
        self.otp = pyotp.TOTP(pyotp.random_base32())

    def _hash_master_password(self, password):
        """
        Hash the provided password using Argon2.
        """
        return self.ph.hash(password)

    def _store_master_password(self, username, password):
        """
        Store the hashed password securely using Keyring.
        """
        keyring.set_password(APP_NAME, username, password)

    def _get_master_password(self, username):
        """
        Retrieve the hashed password for the username.
        Raise ValueError if the username doesn't exist.
        """
        try:
            password = keyring.get_password(APP_NAME, username)
            if password is None:
                raise PasswordManagerError(f"No password associated with username '{username}'.")
            return password
        except keyring.errors.KeyringError as e:
            # Handle specific Keyring errors
            raise PasswordManagerError(f"Keyring error while retrieving password: {e}") from e

    def _validate_master_password(self, password, hashed_password):
        """
        Validate the provided password against the stored hash.
        """
        try:
            if not hashed_password or not password:
                return False

            if self.ph.verify(hashed_password, password):
                return True
        except Exception as e:
            raise e

    def _validate_password(self, password):
        """
        Validate the password against predefined security standards.
        Raise ValueError if the password is weak.
        """
        try:
            score, suggestions = self.validator._security_score(password)
            if score < 2:
                raise Exception("Password is too weak. Suggestions: " + ", ".join(suggestions))
        except Exception as e:
            raise e

    def register(self, username, password):
        """
        Register a new user by storing the hashed password.
        Raise ValueError if the username already exists.
        """
        self._validate_password(password)
        hashed_password = self._hash_master_password(password)
        keyring.set_password(APP_NAME, username, hashed_password)

        # Generate and store a consistent userpin
        userpin = self.generate_userpin(username)
        keyring.set_password(APP_NAME, f"{username}_userpin", userpin)

        return True

    def login(self, username, password):
        """
        Log in by validating the password for the username.
        Return True if valid, otherwise False.
        """
        hashed_password = self._get_master_password(username)
        return self._validate_master_password(password, hashed_password)

    def generate_userpin(self, username):
        """
        Generate a consistent 4-digit userpin based on the username.
        If the userpin already exists, retrieve it from Keyring.
        """
        try:
            existing_userpin = keyring.get_password(APP_NAME, f"{username}_userpin")
            if existing_userpin:
                return existing_userpin
        except keyring.errors.KeyringError:
            pass

        # Generate and return a new userpin if not found
        userpin = str(abs(hash(username)) % 10000).zfill(4)
        return userpin

    def get_userpin(self, username):
        """
        Retrieve the stored userpin for the username.
        """
        userpin = keyring.get_password(APP_NAME, f"{username}_userpin")
        if not userpin:
            raise PasswordManagerError(f"No userpin found for username '{username}'.")
        return userpin

    def verify_otp(self, otp):
        """
        Use pyotp to verify the OTP entered by the user.
        """
        try:
            if not otp:
                raise PasswordManagerError("Please enter the OTP.")
            if not self.otp.verify(otp):
                raise PasswordManagerError("Invalid OTP.")
        except Exception as e:
            raise e
