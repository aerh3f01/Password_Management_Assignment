# A small test environment for secure password management

import os
import hashlib
import random
import string


FILENAME = '2024-2025_USW_Cyber_Esports_App.txt'

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
def passwordStorage(user, password): 

    # Check if the file exists; if not, create it
    if not os.path.exists(FILENAME):
        with open(FILENAME, 'w') as file:
            file.write('')

    # Generate a secure salt for the password
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    # Hash the password
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()

    # Open the file in append mode
    with open(FILENAME, 'a') as file:
        file.write(f"{user}:{salt}:{hashed_password}\n")

    return('Password stored successfully')

def uniqueChecker(username):
    # Check if the file exists; if not, create it
    if not os.path.exists(FILENAME):
        with open(FILENAME, 'w') as file:
            file.write('')
        ## The assumption of no file is no clashing usernames. So return for validity
        return

    with open(FILENAME, 'r') as file:
        for lines in file:
            user, salt, hash = lines.split(':')
            if username == user:
                return("Invalid user: username already taken")
            else:
                continue

def passwordValidity(username, password):
    if not os.path.exists(FILENAME):
        return("No passwords are stored here. Please try storing one.")
    else:
        with open(FILENAME, 'r') as file:
            for lines in file:
                user, salt, hash = lines.split(':')
                format_hash = hash.rstrip('\n')
                if username == user:
                    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
                    if hashed_password == format_hash:
                        print ("valid")
                    else:
                        print ("invalid")
                else:
                    continue


def loginManager():
    print("You have chosen to login...")
    print("loading systems...")
    print()

    print('Please enter a username and password to login.')
    user = input("Please enter your username: ")
    password = input("Please enter your password: ")

    passwordValidity(user, password)

def storeManager():
    print("You have chosen to store a new password...")
    print("loading systems...")
    print()

    # Get the username and password from the user
    username = input('Username: ')
    validity = uniqueChecker(username)
    if validity == "Invalid user: username already taken":
        print(validity)
        return
    else:
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
    
# Create a basic main controller for the program
def main():
    print('Welcome to the password manager')
    print('What would you like to do?')
    print()
    print('1. Create a new user')
    print('2. Login with an existing user')
    print('3. Exit')
    print()

    userInput = input("Select 1, 2 or 3: ")
    if userInput == '1':
        storeManager()
    elif userInput == '2':
        loginManager()
    else:
        return
# Run the main controller
if __name__ == '__main__':
    main()
    #passwordStorage("apples", "codexBrittleScantName'sRook123")
    #passwordValidity("apples", "codexBrittleScantName'sRook123")