# A small test environment for secure password management

import os
import hashlib
import random
import string


'''
The mimimum password standard is 8 characters, with at least one uppercase letter, one lowercase letter, one number, and one special character.
The recommended standard is 13 characters with at least two uppercase letters, two lowercase letters, two numbers, and two special characters.

Anything less returns as invalid and prompts for a user to try again.
'''

def passwordChecker(password):
    if len(password) < 8:
        return 'invalid'
    
    # Define the minimum requirements
    weak_requirements = {
        'length': 8,
        'upper': 1,
        'lower': 1,
        'number': 1,
        'special': 1
    }

    # Define the recommended requirements
    strong_requirements = {
        'length': 13,
        'upper': 2,
        'lower': 2,
        'number': 2,
        'special': 2
    }

    # Check requitements if they are weak, strong or invalid
    password_status = {
        'length': len(password),
        'upper': sum(1 for c in password if c.isupper()),
        'lower': sum(1 for c in password if c.islower()),
        'number': sum(1 for c in password if c.isdigit()),
        'special': sum(1 for c in password if not c.isalnum()),
    }
    
    # Check values against requirements
    if all(password_status[key] >= strong_requirements[key] for key in strong_requirements):
        return 'strong'
    elif all(password_status[key] >= weak_requirements[key] for key in weak_requirements):
        return 'weak'
    else:
        return 'invalid'
    


# Pass the password and username into a text file for storage
def passwordStorage(username, password):
    # Securely store the password and username in a plain text file
    filename = '2024-2025_USW_Cyber_Esports_App.txt'

    # Check if the file exists; if not, create it
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write('')

    # Generate a secure salt for the password
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    # Hash the password
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()

    # Hash the username
    hashed_user = hashlib.sha256((username + salt).encode()).hexdigest()
    
    # Open the file in append mode
    with open(filename, 'a') as file:
        file.write(f"{hashed_user}:{salt}:{hashed_password}\n")

    return('Password stored successfully')



# Create a basic main controller for the program
def main():
    print('Welcome to the password manager')
    print('Please enter a username and password to store securely')

    # Get the username and password from the user
    username = input('Username: ')
    password = input('Password: ')

    while passwordChecker(password) == 'invalid':
        print('Invalid password. Please try again')
        password = input('Password: ')
    if passwordChecker(password) == 'weak':
        print('Weak password. would you like to enter a stronger password?')
        choice = input('Yes or No: ')
        if choice == 'Yes' or choice == 'yes' or choice == 'y':
            password = input('Password: ')
            while passwordChecker(password) == 'invalid':
                print('Invalid password. Please try again')
                password = input('Password: ')
            if passwordChecker(password) == 'weak':
                print('Weak password. Please try again later')
                return
        else:
            return
        
    else:
        print('Strong password.')
        
    # Store the password securely
    passwordStorage(username, password)


# Run the main controller
if __name__ == '__main__':
    main()