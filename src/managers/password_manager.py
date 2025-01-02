import os
import bcrypt
import portalocker
from managers.validation_manager import PasswordValidator

DEFAULT_FILENAME = '{userpin}.PXX'

class PasswordManager:
    """
    Handles secure storage and management of passwords.
    
    This class provides functionalities to:
    - Ensure the password storage file exists.
    - Encrypt and decrypt passwords.
    - Store passwords securely in a file.
    - Check for existing usernames.
    """

    def __init__(self, filename=DEFAULT_FILENAME):
        """
        Initializes the PasswordManager with the given filename.
        
        Parameters:
        filename (str): The name of the file used to store passwords.
        """
        self._filename = filename

    def _ensure_file_exists(self, userpin):
        """Ensures the password storage file exists. Creates it if not present."""
        self._filename = DEFAULT_FILENAME.format(userpin=userpin)
        if not os.path.exists(self._filename):
            try:
                with open(self._filename, 'w') as file:
                    file.write('')  # Create an empty file
            except IOError as e:
                raise IOError(f"Unable to create the file {self._filename}: {e}")
            
    def _encrypt(self, password):
        """Encrypts the given password using bcrypt."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    def _decrypt(self, encrypted_password, password):
        """Decrypts the given password using bcrypt."""
        return bcrypt.checkpw(password.encode(), encrypted_password.encode())
    
    def _username_exists(self, username):
        """Checks if the username already exists in the file."""
        try:
            with open(self._filename, 'r') as file:
                for line in file:
                    if line.startswith(username + ':'):
                        return True
            return False
        except IOError as e:
            raise IOError(f"Error reading the file {self._filename}: {e}")
        
    def load_passwords(self, userpin):
        """Loads the stored passwords from the file."""
        self._ensure_file_exists(userpin)
        passwords = {}
        try:
            with open(self._filename, 'r') as file:
                for line in file:
                    site, username, password = line.strip().split(':')
                    passwords[username] = password
        except IOError as e:
            raise IOError(f"Error reading the file {self._filename}: {e}")

        return passwords
    
    def get_passwords(self, userpin):
        """Returns the stored passwords from the file."""
        return self.load_passwords(userpin)

    def store_password(self, site, username, password):
        """Stores the password securely in the file."""
        try:
            self._ensure_file_exists()
            validity = PasswordValidator.validate(password)
            if not validity:
                ValueError("Password is too weak.")
            encrypted_password = self._encrypt(password)
            with portalocker.Lock(self._filename, 'a') as file:
                file.write(f"{site}:{username}:{encrypted_password}\n")
        except IOError as e:
            raise IOError(f"Error writing to the file {self._filename}: {e}")
        except ValueError as e:
            raise ValueError(f"Error storing the password: {e}")



    def delete_password(self, site, username):
        """Deletes the password associated with the given username."""
        self._ensure_file_exists()
        temp_filename = self._filename + '.tmp'
        with portalocker.Lock(self._filename, 'r') as file, open(temp_filename, 'w') as temp_file:
            for line in file:
                if not line.startswith(username + ':'):
                    temp_file.write(line)
        os.replace(temp_filename, self._filename)

    def add_password(self, site, username, password):
        """Adds a new password to the list."""
        if not self._username_exists(username):
            self.store_password(site, username, password)
        else:
            raise ValueError("Username already exists.")

