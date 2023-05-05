from .schemas import *
from .models import *

from .validations import *
from . import calculation

from datetime import datetime


async def create_user(user: UserCreate) -> UserModel:
    new_user = UserModel(
        password=user.password,
        login=user.login,
        role="user",  # TODO change to correct role
        name=user.name,
        surname=user.surname,
        patronymic=user.patronymic,
        email=user.email,
    )
    await new_user.create()

    return new_user


async def get_user(user_id: str) -> Optional[UserModel]:
    user = await UserModel.get(id=user_id)
    return user or None


async def edit_user(updt_user: UserUpdate, user_id: str) -> Optional[UserModel]:
    user = await UserModel.get(id=user_id)
    if user:
        user.name = updt_user.name
        user.surname = updt_user.surname
        user.patronymic = updt_user.patronymic
        await user.update()
        return user
    return None


async def delete_user(user_id: str):
    user = await UserModel.get(id=user_id)
    if user:
        await user.delete()


async def create_student_group(stg: StudentGroupCreate) -> Optional[StudentGroupModel]:
    teacher = await get_user(stg.teacher_id)
    if not teacher:
        return None

    student_group = StudentGroupModel(
        title=stg.title, teacher=teacher)

    await student_group.create()
    student_group.connect_code = student_group.id
    await student_group.update()

    return student_group


async def get_student_group(stg_id: str) -> Optional[StudentGroupModel]:
    student_group = await StudentGroupModel.get(id=stg_id)
    return student_group or None


async def edit_student_group(stg: StudentGroupUpdate, stg_id: str) -> Optional[StudentGroupModel]:
    student_group = await StudentGroupModel.get(id=stg_id)
    if student_group:
        student_group.title = stg.title
        await student_group.update()
        return student_group
    else:
        return None


async def delete_student_group(stg_id: str):
    student_group = await StudentGroupModel.get(id=stg_id)
    if student_group:
        await student_group.delete()


async def create_homework(hw: HomeworkCreate) -> Optional[HomeworkModel]:
    student_group = await get_student_group(hw.student_group_id)

    if not student_group:
        return None

    homework = HomeworkModel(
        title=hw.title,
        files=hw.files,
        student_group=student_group,
        uploaded_at=datetime.now(),
        deadline=hw.deadline,
        last_updated_at=datetime.now(),
        points=hw.points,
        mark_formula=hw.mark_formula
    )
    await homework.create()

    return homework


async def get_homework(hw_id: str) -> Optional[HomeworkModel]:
    homework = await HomeworkModel.get(id=hw_id)
    return homework or None


async def edit_homework(hw: HomeworkUpdate, hw_id: str) -> Optional[HomeworkModel]:
    homework = await HomeworkModel.get(id=hw_id)
    if homework:
        homework.title = hw.title
        homework.files = hw.files
        homework.deadline = hw.deadline
        homework.points = hw.points
        homework.mark_formula = hw.mark_formula
        homework.last_updated_at = datetime.now()

        await homework.update()

        recalculate_homework_marks(homework)

        return homework
    else:
        return None


async def delete_homework(hw_id: str):
    homework = await HomeworkModel.get(id=hw_id)
    if homework:
        await homework.delete()


async def create_submission(sub: SubmissionCreate) -> Optional[SubmissionModel]:
    student = await get_user(sub.student_id)
    homework = await get_homework(sub.homework_id)

    if not student or not homework:
        return None

    points = [0.0] * len(homework.points)

    submission = SubmissionModel(
        student=student,
        homework=homework,
        points=points,
        start_submit=datetime.now(),
        last_updated_at=datetime.now()
    )

    await submission.create()

    return submission


async def get_submission(sub_id: str) -> Optional[SubmissionModel]:
    submission = await SubmissionModel.get(id=sub_id)
    return submission or None


async def edit_submission(sub: SubmissionUpdate, sub_id) -> Optional[SubmissionModel]:
    submission = await SubmissionModel.get(id=sub_id)
    if submission:
        submission.fine = sub.fine
        submission.points = sub.points
        submission.last_updated_at = datetime.now()
        submission.mark = calculation.calculate_mark(
            submission.homework.points, sub.points, submission.homework.mark_formula, sub.fine)

        await submission.update()
        return submission
    else:
        return None


async def delete_submission(sub_id: str):
    submission = await SubmissionModel.get(id=sub_id)
    if submission:
        await submission.delete()


# ------------------------ ADDITIONAL METHODS ------------------------


def get_all_submission_by_homework(hw: HomeworkModel) -> list:
    subs = SubmissionModel.objects(homework=hw)
    return list(subs)


def recalculate_homework_marks(hw: HomeworkModel):
    subs = get_all_submission_by_homework(hw)
    for sub in subs:
        sub.mark = calculation.calculate_mark(
            hw.points, sub.points, hw.mark_formula, sub.fine)
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
    stgs = StudentGroupModel.objects(teacher=user)
    return list(stgs)


def remove_user_from_student_group(student_group_id: str, user_id: str):
    student_group = StudentGroupModel.objects.get(id=student_group_id)
    user = UserModel.objects.get(id=user_id)
    if student_group in user.students_groups:
        user.students_groups.remove(student_group)
        user.save()
