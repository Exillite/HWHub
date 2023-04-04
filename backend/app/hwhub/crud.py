from .schemas import *
from .models import *

from .validations import *
from . import calculation

import datetime

def create_user(user: UserCreate):
    # user.password = user.password.encode('utf-8')
    new_user = UserModel(role="student", 
                login=user.login,
                name=user.name, 
                surname=user.surname, 
                patronymic=user.patronymic,
                email=user.email,
                password=user.password, 
                is_active=True)
    new_user.save()
    
    return new_user

def get_user(user_id: str) -> UserModel:
    user = UserModel.objects(pk=user_id).first()
    if user:
        return user
    return None

def edit_user(updt_user: UserUpdate, user_id: str) -> UserModel:
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


def create_student_group(stg: StudentGroupCreate) -> StudentGroupModel:
    teacher = get_user(stg.teacher_id)
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


def create_homework(hw: HomeworkCreate) -> HomeworkModel:
    student_group = get_student_group(hw.student_group_id)
    
    homework = HomeworkModel(
        title=hw.title,
        file=hw.file,
        student_group=student_group,
        uploaded_at=datetime.datetime.now(),
        deadline=hw.deadline,
        last_updated_at=datetime.datetime.now(),
        points=hw.points,
        mark_formula=hw.mark_formula
    )
    homework.save()
    
    return homework

def get_homework(hw_id: str) -> HomeworkModel:
    homework = HomeworkModel.objects(pk=hw_id).first()
    if homework:
        return homework
    else:
        return None

def edit_homework(hw: HomeworkUpdate, hw_id: str) -> HomeworkModel:
    homework = HomeworkModel.objects(pk=hw_id).first()
    if homework:
        homework.title = hw.title
        homework.file = hw.file
        homework.deadline = hw.deadline
        homework.points = hw.points
        homework.mark_formula = hw.mark_formula
        homework.last_updated_at = datetime.datetime.now()
                
        homework.save()
        
        recalculate_homework_marks(homework)
        
        return homework
    else:
        return None

def delete_homework(hw_id: str):
    homework = HomeworkModel.objects(pk=hw_id).first()
    homework.delete()


def create_submission(sub: SubmissionCreate) -> SubmissionModel:
    student = get_user(sub.student_id)
    homework = get_homework(sub.homework_id)
    
    points = [0.0] * len(homework.points)
    
    submission = SubmissionModel(
        student=student,
        homework=homework,
        points=points,
        start_submit=datetime.datetime.now(),
        last_updated_at=datetime.datetime.now()
    )
    
    submission.save()
    
    return submission

def get_submission(sub_id: str) -> SubmissionModel:
    submission = SubmissionModel.objects(pk=sub_id).first()
    if submission:
        return submission
    else:
        return None
    
def edit_submission(sub: SubmissionUpdate, sub_id) -> SubmissionModel:
    submission = SubmissionModel.objects(pk=sub_id).first()
    if submission:
        submission.fine = sub.fine
        submission.points = sub.fine
        submission.last_updated_at = datetime.datetime.now()
        submission.mark = calculation.calculate_mark(submission.homework.points, sub.points, submission.homework.mark_formula, sub.fine)
        
        submission.save()
        return submission
    else:
        return None

def delete_submission(sub_id: str) -> SubmissionModel:
    submission = SubmissionModel.objects(pk=sub_id).first()
    submission.delete()


# ------------------------ ADDITIONAL METHODS ------------------------


def get_all_submission_by_homework(hw: HomeworkModel) -> list:
    subs = SubmissionModel.objects(homework=hw)
    return list(subs)


def recalculate_homework_marks(hw: HomeworkModel):
    subs = get_all_submission_by_homework(hw)
    for sub in subs:
        sub.mark = calculation.calculate_mark(hw.points, sub.points, hw.mark_formula, sub.fine)
        sub.save()

def get_homeworks_by_students_group(std: StudentGroupModel) -> list:
    homeworks = HomeworkModel.objects(student_group=std)
    return list(homeworks)


def get_submissions_by_homework(hw: HomeworkModel) -> list:
    subs = SubmissionModel.objects(homework=hw)
    return list(subs)


def get_submission_by_homework_and_student(hw: HomeworkModel, user: UserModel) -> SubmissionModel:
    sub = SubmissionModel.objects(homework=hw, student=user).first()
    return sub


def get_submissions_by_student(user: UserModel) -> list:
    subs = SubmissionModel.objects(student=user)
    return list(subs)


def get_user_by_login(login: str) -> UserModel:
    user = UserModel.objects(login=login).first()
    if user:
        return user
    return None


def get_students_from_students_group(std: StudentGroupModel):
    return UserModel.objects(students_groups=std, role="student")

def get_consultants_from_students_group(std: StudentGroupModel):
    return UserModel.objects(students_groups=std, role="consultant")


def get_students_group_by_teacher(teacher_id):
    user = UserModel.objects(pk=teacher_id).first()
    stgs = StudentGroup.objects(teacher=user)
    return list(stgs)


def remove_user_from_student_group(student_group_id: str, user_id: str):
    student_group = StudentGroupModel.objects.get(id=student_group_id)
    user = UserModel.objects.get(id=user_id)
    if student_group in user.students_groups:
        user.students_groups.remove(student_group)
        user.save()
