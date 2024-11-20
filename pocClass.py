import os
import hashlib
import random
import string

class PasswordValidator:
    """Handles password validation based on predefined security standards."""
    
    def __init__(self):
        self.weak_requirements = {
            'length': 8,
            'upper': 1,
            'lower': 1,
            'number': 1,
            'special': 1
        }

        self.strong_requirements = {
            'length': 13,
            'upper': 2,
            'lower': 2,
            'number': 2,
            'special': 2
        }

    def validate(self, password):
        if len(password) < 8:
            return 'invalid'

        password_status = {
            'length': len(password),
            'upper': sum(1 for c in password if c.isupper()),
            'lower': sum(1 for c in password if c.islower()),
            'number': sum(1 for c in password if c.isdigit()),
            'special': sum(1 for c in password if not c.isalnum()),
        }

        if all(password_status[key] >= self.strong_requirements[key] for key in self.strong_requirements):
            return 'strong'
        elif all(password_status[key] >= self.weak_requirements[key] for key in self.weak_requirements):
            return 'weak'
        else:
            return 'invalid'


class PasswordManager:
    """Handles secure storage and management of passwords."""
    
    def __init__(self, filename='passwords.txt'):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                file.write('')

    def _generate_salt(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    def _hash(self, value, salt):
        return hashlib.sha256((value + salt).encode()).hexdigest()

    def store_password(self, username, password):
        salt = self._generate_salt()
        hashed_user = self._hash(username, salt)
        hashed_password = self._hash(password, salt)

        with open(self.filename, 'a') as file:
            file.write(f"{hashed_user}:{salt}:{hashed_password}\n")
        
        return 'Password stored successfully'


class MainController:
    """Main program controller for user interaction."""
    
    def __init__(self):
        self.validator = PasswordValidator()
        self.manager = PasswordManager()

    def run(self):
        print('Welcome to the password manager')
        username = input('Username: ')
        password = input('Password: ')

        while self.validator.validate(password) == 'invalid':
            print('Invalid password. Please try again.')
            password = input('Password: ')

        if self.validator.validate(password) == 'weak':
            print('Weak password. Would you like to enter a stronger password?')
            if input('Yes or No: ').lower() in ['yes', 'y']:
                password = input('Password: ')
                while self.validator.validate(password) == 'invalid':
                    print('Invalid password. Please try again.')
                    password = input('Password: ')
                if self.validator.validate(password) == 'weak':
                    print('Weak password. Please try again later.')
                    return
            else:
                return
        else:
            print('Strong password.')

        print(self.manager.store_password(username, password))


if __name__ == '__main__':
    MainController().run()
