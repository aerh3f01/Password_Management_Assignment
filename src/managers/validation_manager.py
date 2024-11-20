class PasswordValidator:
    """Handles password validation based on predefined security standards."""
    
    def __init__(self):
        """
        Initializes the PasswordValidator with predefined security standards.
        
        weak_requirements: Minimum requirements for a weak password.
        strong_requirements: Minimum requirements for a strong password.
        """
        self.weak_requirements = {
            'length': 8,
            'upper': 1,
            'lower': 1,
            'number': 1,
            'special': 1
        }

        self.strong_requirements = {
            'length': 13,
            'lower': 2,
            'number': 2,
            'special': 2
        }

    def validate(self, password):

        """
        Validates the given password based on predefined security standards.

        Args:
        password (str): The password to validate.

        Returns:
        str: 'invalid' if the password does not meet the weak requirements,
        'weak' if the password meets the weak requirements but not the strong requirements,
        'strong' if the password meets the strong requirements.
        """
                
        if len(password) < self.weak_requirements['length']:
            return 'invalid'

        password_status = {
            'length': len(password),
            'upper': sum(1 for c in password if c.isupper()),
            'lower': sum(1 for c in password if c.islower()),
            'number': sum(1 for c in password if c.isdigit()),
            'special': sum(1 for c in password if not c.isalnum()),
        }

        if self._meets_requirements(password_status, self.strong_requirements):
            return 'strong'
        elif self._meets_requirements(password_status, self.weak_requirements):
            return 'weak'
        return 'invalid'

    def _meets_requirements(self, password_status, requirements):
        return all(password_status[key] >= requirements[key] for key in requirements)
