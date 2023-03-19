import re
import bcrypt

from .models import *
from .schemas import *

def get_hashed_password(plain_text_password: str) -> str:
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def check_password(plain_text_password: str, hashed_password: str) -> bool:
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)

def email_validation(email: str) -> bool:
    # check is email correct
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def password_validation(password: str) -> bool:
    # check is password correct
    return len(password) >= 8

def validation_create_user(user: UserCreate):
    # check is user correct and return is_correct and status code
    if email_validation(user.email):
        return False, 202
    if UserModel.objects(email=user.email).first():
        return False, 202

    if password_validation(user.password):
        return False, 203
    
    return True, 200

def validation_login_user(user: UserLogin):
    # check is user correct and return is_correct and status code
    if email_validation(user.email):
        return False, 202

    if password_validation(user.password):
        return False, 203
    
    return True, 200
