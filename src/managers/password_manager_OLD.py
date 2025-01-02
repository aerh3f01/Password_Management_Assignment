import os
import hashlib
import random
import string
import portalocker

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

    def _store_master_password(self, site, username, password):
        """
        Stores a password securely for a given username.
        
        Parameters:
        site (str): The website associated with the password.
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
                portalocker.lock(file, portalocker.LOCK_EX)
                try:
                    file.write(f"{site}:{username}:{salt}:{hashed_password}\n")
                finally:
                    portalocker.unlock(file)
            return 'Password stored successfully'
        except IOError as e:
            raise IOError(f"An error occurred while writing to the file {self.filename}: {e}")



    def _verify_password(self, username, password):
        """
        Verifies the provided password for the given username.
        
        Parameters:
        username (str): The username to verify.
        password (str): The password to verify.
        
        Returns:
        bool: True if the password is correct, False otherwise.
        
        Raises:
        ValueError: If the username does not exist or the password is incorrect.
        """
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    _, stored_username, salt, hashed_password = line.strip().split(':')
                    if stored_username == username:
                        if self._hash(password, salt) == hashed_password:
                            return True
                        else:
                            return False
                raise ValueError('Username not found')
        except IOError as e:
            raise IOError(f"An error occurred while reading the file {self.filename}: {e}")
            
    def load_passwords(self):
        """
        Loads and returns all stored passwords.
        
        Returns:
        list: A list of tuples containing the username and hashed password.

        Raises:
        IOError: If the file cannot be read.
        """
        try:
            with open(self.filename, 'r') as file:
                passwords = []
                for line in file:
                    site, stored_username, _, hashed_password = line.strip().split(':')
                    passwords.append((site, stored_username, hashed_password))
                
        except IOError as e:
            raise IOError(f"An error occurred while reading the file {self.filename}: {e}")
        
    def remove_password(self,site,username):
        """
        Removes the stored password for the given username.
        
        Parameters:
        username (str): The username associated with the password.
        
        Returns:
        str: A message indicating the password was removed successfully.
        
        Raises:
        ValueError: If the username does not exist.
        IOError: If the file cannot be written to.
        """
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
            with open(self.filename, 'w') as file:
                for line in lines:
                    stored_site, stored_username, _, _ = line.strip().split(':')
                    if stored_username != username and stored_site != site:
                        file.write(line)
                return 'Password removed successfully'
        except IOError as e:
            raise IOError(f"An error occurred while writing to the file {self.filename}: {e}")
        except ValueError as e:
            raise ValueError(f"An error occurred while verifying the password: {e}")
    def get_passwords(self):
        
        try:
            with open(self.filename, 'r') as file:
                passwords = []
                for line in file:
                    site, user, salt, password = line.strip().split(':')
                    clean_password = self._unencrypt_password(password, salt)
                    passwords.append({'website': site, 'username': user, 'password': clean_password})
                return passwords
        except IOError as e:
            raise IOError(f"An error occurred while reading the file {self.filename}: {e}")
        except ValueError as e:
            raise ValueError(f"An error occurred while verifying the password: {e}")
        
    def add_password(self, website, username, password):
        """
        Adds a new password for the given username.
        
        Parameters:
        username (str): The username associated with the password.
        password (str): The password to be stored.
        
        Returns:
        str: A message indicating the password was added successfully.
        
        Raises:
        IOError: If the file cannot be written to.
        """
        return self._store_password(website, username, password)
    
    def delete_password(self, site, username):
        """
        Deletes the password for the given username.
        
        Parameters:
        username (str): The username associated with the password.
        
        Returns:
        str: A message indicating the password was deleted successfully.
        
        Raises:
        ValueError: If the username does not exist.
        IOError: If the file cannot be written to.
        """
        return self.remove_password(site, username)

