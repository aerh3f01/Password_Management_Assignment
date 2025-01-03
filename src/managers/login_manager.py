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
                PasswordManagerError(f"No password associated with username '{username}'.")
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
                Exception("Password is too weak. Suggestions: " + ", ".join(suggestions))
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
        self.generate_userpin(username)
        self.generate_otp(username)
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
        Generate a unique 4 digit userpin for the user.
        """
        pass

    def get_userpin(self):
        """
        Retrieve the userpin for the user.
        """
        pass

    def verify_otp(self, otp):
        """
        Use pyotp to verify the OTP entered by the user.
        """
        try:
            if not otp:
                PasswordManagerError("Please enter the OTP.")
            pyotp.TOTP.verify(otp)
        except Exception as e:
            raise e

