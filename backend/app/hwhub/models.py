from beanie import Document, PydanticObjectId, Link
from pydantic import EmailStr
from typing import Optional, List
from datetime import datetime


class UserModel(Document):
    password: str
    login: str
    role: str
    name: str
    surname: str
    patronymic: str
    email: EmailStr
    vk_id: Optional[str] = None
    telegram_id: Optional[str] = None
    students_groups: List["StudentGroupModel"] = []
    is_active: bool = True


class StudentGroupModel(Document):
    title: str
    teacher: Link[UserModel]
    connect_code: Optional[str] = None
    is_active: bool = True


class HomeworkModel(Document):
    title: str
    file: List[str]
    student_group: Link[StudentGroupModel]
    uploaded_at: datetime
    deadline: datetime
    last_updated_at: datetime
    points: List[float]
    mark_formula: str
    is_active: bool = True


class SubmissionModel(Document):
    student: Link[UserModel]
    homework: Link[HomeworkModel]
    points: List[float]
    fine: float
    mark: float
    start_submit: datetime
    last_updated_at: datetime
    is_active: bool = True


__db_models__ = [UserModel, StudentGroupModel, HomeworkModel, SubmissionModel]
