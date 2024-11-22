# Uses the PasswordValidator class to validate
# Backups with zxcvbn algorithm to give a security score

from zxcvbn import zxcvbn

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

    def _security_score(self, password):
        """
        Returns the security score of the given password using the zxcvbn algorithm.
        Also takes feedback from the zxcvbn algorithm to improve the password.

        Args:
        password (str): The password to evaluate.

        Returns:
        int: The security score of the password.
        str: The feedback from the zxcvbn algorithm.
        """
        result = zxcvbn(password)
        print(result)

        return result['score'], result['feedback']['suggestions']
    

    def _min_validation(self, password):

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

    def validate(self, password):
        """ 
        Controls the validation program flow.
        Sends to the minimum validation and security score functions.
        """
        min_validation = self._min_validation(password)
        if min_validation == 'invalid':
            return 'invalid'
        else:
            security_score, suggestions = self._security_score(password)
            if security_score == 4:
                return 'strong'
            elif security_score >= 3:
                return 'weak', suggestions
            else:
                return 'invalid', suggestions