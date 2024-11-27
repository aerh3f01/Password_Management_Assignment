import string
from secrets import SystemRandom, choice
class PasswordGeneration:
    """
    Handles automatic password generation with specific requirements.
    """
    def __init__(self):
        # Minimum requirements for the password
        self.length = 15
        self.uppercase = 2
        self.numbers = 2
        self.specials = 2

    def generate_secure_password(self):
        """
        Generate a secure password meeting the defined criteria.
        """
        # Character sets
        upperCase = string.ascii_uppercase
        lowerCase = string.ascii_lowercase
        numbers = string.digits
        specials = string.punctuation

        # Build the password with required characters
        password = [
            *(choice(upperCase) for _ in range(self.uppercase)),
            *(choice(numbers) for _ in range(self.numbers)),
            *(choice(specials) for _ in range(self.specials)),
            *(choice(upperCase + lowerCase + numbers + specials) 
              for _ in range(self.length - self.uppercase - self.numbers - self.specials))
        ]

        # Shuffle and return as a string
        SystemRandom().shuffle(password)
        return ''.join(password)
