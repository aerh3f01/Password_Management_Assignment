import string
import secrets

class PasswordGeneration:
    """
    Handle Automatic Password Generation
    """

    def __init__(self):
        self.length = 18
        self.use_upper = True
        self.use_nums = True
        self.use_specials = True

    def generate_password(self):
        char = string.ascii_lowercase
        if self.use_upper:
            char += string.ascii_uppercase
        if self.use_nums:
            char += string.digits
        if self.use_special:
            char += string.punctuation
        
        password = "".join(secrets.choice(char) for i in range (self.length))

        return password

