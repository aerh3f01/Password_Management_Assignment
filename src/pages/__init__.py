# Initialise the frame modules

from .startFrame import StartPage
from .loginFrame import LoginPage
from .registerFrame import RegisterPage
from .passwordFrame import PasswordsPage


## Export the classes

__all__ = [
    'StartPage',
    'LoginPage',
    'RegisterPage',
    'PasswordsPage'
]