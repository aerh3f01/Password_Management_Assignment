import os
import hashlib
import random
import string
import fcntl

DEFAULT_FILENAME = 'passwords.txt'
SALT_LENGTH = 8

class PasswordManager:
    """
    Handles secure storage and management of passwords.
    
    This class provides functionalities to:
    - Ensure the password storage file exists.
    - Generate a random salt for password hashing.
    - Hash passwords using SHA-256 with a salt.
    - Store passwords securely in a file.
    - Check for existing usernames.
    """
    
    def __init__(self, filename=DEFAULT_FILENAME):
        """
        Initializes the PasswordManager with the given filename.
        
        Parameters:
        filename (str): The name of the file used to store passwords.
        """
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensures the password storage file exists. Creates it if not present."""
        if not os.path.exists(self.filename):
            try:
                with open(self.filename, 'w') as file:
                    file.write('')  # Create an empty file
            except IOError as e:
                raise IOError(f"Unable to create the file {self.filename}: {e}")

    def _generate_salt(self):
        """Generates a random salt of predefined length."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=SALT_LENGTH))

    def _hash(self, value, salt):
        """
        Hashes the given value with the provided salt using SHA-256.
        
        Parameters:
        value (str): The value to hash.
        salt (str): The salt to append to the value before hashing.
        
        Returns:
        str: The resulting hash.
        """
        return hashlib.sha256((value + salt).encode()).hexdigest()
    
    def _username_exists(self, username):
        """Checks if the username already exists in the file."""
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    stored_username = line.split(':')[0]
                    if stored_username == username:
                        return True
            return False
        except IOError as e:
            raise IOError(f"An error occurred while reading the file {self.filename}: {e}")

    def store_password(self, username, password):
        """
        Stores a password securely for a given username.
        
        Parameters:
        username (str): The username associated with the password.
        password (str): The password to be stored.
        
        Returns:
        str: A message indicating the password was stored successfully.
        
        Raises:
        IOError: If the file cannot be written to.
        """
        if self._username_exists(username):
            return 'Username already exists'
        
        salt = self._generate_salt()
        hashed_password = self._hash(password, salt)
        
        try:
            with open(self.filename, 'a') as file:
                # Lock the file to prevent race conditions
                fcntl.flock(file, fcntl.LOCK_EX)
                try:
                    file.write(f"{username}:{salt}:{hashed_password}\n")
                finally:
                    fcntl.flock(file, fcntl.LOCK_UN)
            return 'Password stored successfully'
        except IOError as e:
            raise IOError(f"An error occurred while writing to the file {self.filename}: {e}")
    
