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


def get_all_students_groups() -> List[StudentGroup]:
    # get all student groups
    student_groups = []
    all_student_groups = StudentGroupModel.objects(is_active=True)
    for student_group in all_student_groups:
        student_groups.append(model_to_student_group(student_group))
    return student_groups

def get_student_group(student_group_id: str) -> StudentGroup:
    # get student group data
    student_group = StudentGroupModel.objects(pk=student_group_id).first()
    if student_group:
        return model_to_student_group(student_group)
    return None

def generate_student_group_code() -> str:
    # generate student group unique code wirh length N
    N = 6
    student_group_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
    while StudentGroupModel.objects(code=student_group_code).first():
        student_group_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
    return student_group_code

def create_student_group(student_group: StudentGroupCreate) -> StudentGroup:
    # add new student group to database
    new_student_group = StudentGroupModel(title=student_group.title,
                                          teacher=student_group.teacher,
                                          is_active=True)
    new_student_group.save()

    new_student_group.code = generate_student_group_code()
    new_student_group.save()

    return new_student_group

def edit_student_group(updt_student_group: StudentGroupUpdate, student_group_id: str) -> StudentGroup:
    # edit student group data
    student_group = StudentGroupModel.objects(pk=student_group_id).first()
    if student_group:
        student_group.title = updt_student_group.title
        student_group.save()
        return student_group
    return None


