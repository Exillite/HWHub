from backend.app.hwhub.models import *
from backend.app.hwhub.schemas import *

import validations

def registration_user(user: UserCreate) -> User:
    # add new user to database
    new_user = UserModel(role="student", 
                    name=user.name, 
                    surname=user.surname, 
                    patronymic=user.patronymic,
                    email=user.email, 
                    password=validations.get_hashed_password(user.password), 
                    is_active=True)
    new_user.save()
    return new_user

def login_user(login_user: UserLogin) -> User:
    # check is login data correct and return user if correct or None if not
    user = UserModel.objects(email=login_user.email).first()
    if user and validations.check_password(login_user.password, user.password):
        return user
    return None