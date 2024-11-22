import string
import secrets

class PasswordGeneration:
    """
    Handle Automatic Password Generation
    """

    def __init__(self):
        # Define minimum requirements
        self.length = 18
        self.upperCase = 2
        self.numbers = 2
        self.specials = 2

    def generate_password(self):
        """
        Generate a password with the defined requirements.
        """
        # Define the character sets
        upperCase = string.ascii_uppercase
        lowerCase = string.ascii_lowercase
        numbers = string.digits
        specials = string.punctuation

        # Initialize the password
        password = []

        # Add the required characters
        password.extend(secrets.choice(upperCase) for _ in range(self.upperCase))
        password.extend(secrets.choice(numbers) for _ in range(self.numbers))
        password.extend(secrets.choice(specials) for _ in range(self.specials))

        # Add the remaining characters
        remaining = self.length - self.upperCase - self.numbers - self.specials
        password.extend(secrets.choice(upperCase + lowerCase + numbers + specials) for _ in range(remaining))

        # Shuffle the password
        secrets.SystemRandom().shuffle(password)

        return ''.join(password)