import string
from app.schemas import *
from app.models import *

from validations import *

import datetime
import random

def create_user(user: UserCreate):
    new_user = UserModel(role="student", 
                name=user.name, 
                surname=user.surname, 
                patronymic=user.patronymic,
                email=user.email, 
                password=get_hashed_password(user.password), 
                is_active=True)
    new_user.save()
    
    return new_user

def get_user(user_id: str) -> User:
    # get user data
    usr_mdl = UserModel.objects(pk=user_id).first()
    user = model_to_user(usr_mdl)
    if user:
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

def delete_user(user_id: str):
    user = UserModel.objects(pk=user_id).first()
    user.delete()


def create_student_group(stg: StudentGroupCreate):
    teacher = get_user(stg.teacher.pk)
    student_group = StudentGroupModel(
        title=stg.title,
        teacher=teacher,
    )
    
    student_group.save()
    student_group.connect_code = student_group.pk
    
    return student_group

def get_student_group(stg_id: str) -> StudentGroupModel:
    student_group = StudentGroupModel.objects(pk=stg_id).first()
    if student_group:
        return student_group
    else:
        return None

def edit_student_group(stg: StudentGroupUpdate, stg_id:str) -> StudentGroupModel:
    student_group = StudentGroupModel.objects(pk=stg_id).first()
    if student_group:
        student_group.title = stg.title
        
        student_group.save()
        return student_group
    else:
        return None
    
def delete_student_group(stg_id: str):
    student_group = StudentGroupModel.objects(pk=stg_id).first()
    student_group.delete()
