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

def model_to_user(user: UserModel) -> User:
    # convert user model to user schema
    return User(pk=user.pk,
                role=user.role,
                name=user.name,
                surname=user.surname,
                patronymic=user.patronymic,
                email=user.email,
                vk_id=user.vk_id,
                telegram_id=user.telegram_id,
                students_groups=user.students_groups,
                is_active=user.is_active)

def model_to_student_group(student_group: StudentGroupModel) -> StudentGroup:
    # convert student group model to student group schema
    return StudentGroup(pk=student_group.pk,
                        title=student_group.title,
                        teacher=model_to_user(student_group.teacher),
                        connect_code=student_group.connect_code,
                        is_active=student_group.is_active)