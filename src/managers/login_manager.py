# A registration and login manager for the application

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import keyring

APP_NAME = "pass_man"

class LoginManager:
    """
    Handles user registration and login with secure password hashing and storage.
    """
    def __init__(self):
        self.ph = PasswordHasher()

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
        password = keyring.get_password(APP_NAME, username)
        if password is None:
            raise ValueError("No password associated with the given username.")
        return password

    def _validate_master_password(self, password, hashed_password):
        """
        Validate the provided password against the stored hash.
        """
        try:
            self.ph.verify(hashed_password, password)
            return True
        except VerifyMismatchError:
            return False

    def register(self, username, password):
        """
        Register a new user by storing their hashed password.
        Raise ValueError if the username already exists.
        """
        if keyring.get_password(APP_NAME, username):
            raise ValueError("Username already exists.")
        hashed_password = self._hash_master_password(password)
        self._store_master_password(username, hashed_password)

    def login(self, username, password):
        """
        Log in by validating the password for the username.
        Return True if valid, otherwise False.
        """
        hashed_password = self._get_master_password(username)
        return self._validate_master_password(password, hashed_password)
