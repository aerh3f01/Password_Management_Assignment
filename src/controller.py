import sys
from managers import PasswordManager, PasswordValidator, PasswordGeneration
from getpass import getpass

class MainController:
    """Main program controller for user interaction."""
    
    def __init__(self):
        """
        Initializes the MainController with a PasswordValidator and PasswordManager.
        """
        self.validator = PasswordValidator()
        self.manager = PasswordManager()

    def get_valid_password(self):
        """Prompts the user for a valid password and handles validation logic."""
        while True:
            try:
                password = getpass('Password: ')
                if not password:
                    raise ValueError("Password cannot be empty.")
                
                validation_result = self.validator.validate(password)
                
                if validation_result == 'strong':
                    print('Strong password.')
                    return password
                elif validation_result == 'weak':
                    print('Weak password. Would you like to enter a stronger password?')
                    if input('Yes or No: ').strip().lower() in ['yes', 'y']:
                        continue
                    else:
                        print('Weak password accepted.')
                        return password
                else:
                    print('Invalid password. Please try again.')
            except ValueError as ve:
                print(f"Error: {ve}")
            except Exception as e:
                try:
                    # Attempt to log the error to a file
                    with open('error.log', 'a') as file:
                        file.write(f"An error occurred: {e}\n")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                finally:
                    print("An unexpected error occurred. Please try again.")
                    continue  # Allow the user to retry

    

    def run(self):
        """Runs the main program loop."""
        print('Welcome to the password manager!')
        print('Please enter your username and password.')
        
        try:
            username = input('Username: ').strip()
            if not username:
                raise ValueError("Username cannot be empty.")
            
            # Auto generate password or manual input
            print('Would you like to auto-generate a password?')
            if input('Yes or No: ').strip().lower() in ['yes', 'y']:
                password = PasswordGeneration().generate_password()
                print(f'Generated password: " {password} "')
                print('Please keep this master password safe.')
            else:
                password = self.get_valid_password()
            # Store the password securely
            result = self.manager.store_password(username, password)
            print(result)
        except ValueError as ve:
            print(f"Error: {ve}")
        except IOError as e:
            print(f"An error occurred while storing the password: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    MainController().run()