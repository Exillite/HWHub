import string
from app.schemas import *
from app.models import *

from validations import *

import datetime
import random

def registration_user(user: UserCreate) -> User:
    # add new user to database
    new_user = UserModel(role="student", 
                     name=user.name, 
                     surname=user.surname, 
                     patronymic=user.patronymic, 
                     email=user.email, 
                     password=get_hashed_password(user.password), 
                     is_active=True)
    new_user.save()
    return new_user

def login_user(login_user: UserLogin) -> User:
    # check is login data correct and return user if correct or None if not
    user = UserModel.objects(email=login_user.email).first()
    if user and check_password(login_user.password, user.password):
        return user
    return None

def edit_user(updt_user: UserUpdate, user_id: str) -> User:
    # edit user data
    user = UserModel.objects(pk=user_id).first()
    if user:
        user.name = updt_user.name
        user.surname = updt_user.surname
        user.patronymic = updt_user.patronymic
        user.save()
        return user
    return None

def get_user(user_id: str) -> User:
    # get user data
    usr_mdl = UserModel.objects(pk=user_id).first()
    user = model_to_user(usr_mdl)
    if user:
        return user
    return None

def delete_user(user_id: str):
    user = UserModel.objects(pk=user_id).first()
    user.delete()


# def create_student_group()
