import re
import bcrypt

from .models import *
from .schemas import *


def get_hashed_password(plain_text_password: str) -> str:
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return str(bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt()))


def check_password(plain_text_password: str, hashed_password: str) -> bool:
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))


def email_validation(email: str) -> bool:
    # check is email correct
    return re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email) is not None


def password_validation(password: str) -> bool:
    # check is password correct
    return len(password) >= 8


def validation_create_user(user: UserCreate):
    """
    Parameters:
        user (UserCreate): A UserCreate object representing the user information to be validated.

    Returns:
        A tuple containing:
        A boolean value indicating whether the user information is valid or not.
        A status code indicating the reason for invalidity.

    Status codes:
        200: User information is valid.
        202: User email is invalid or already exists.
        203: User password is invalid.
        204: User with this login already exists.

    Note:
        This function does not create a new user. It only validates the user information provided.    
    """
    # check is user correct and return is_correct and status code
    if not email_validation(user.email):
        return False, 202
    if not password_validation(user.password):
        return False, 203
    if UserModel.find_one(UserModel.email == user.email):
        return False, 202
    if UserModel.find_one(UserModel.login == user.login):
        return False, 204

    return True, 200
