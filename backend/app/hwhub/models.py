from beanie import Document, PydanticObjectId, Link
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserModel(BaseModel):
    password: str
    login: str
    role: str
    name: str
    surname: str
    patronymic: str
    email: EmailStr
    vk_id: Optional[int] = None
    telegram_id: Optional[int] = None
    students_groups: List["StudentGroupModel"] = []
    is_active: bool = True


class StudentGroupModel(BaseModel):
    title: str
    teacher: Link[UserModel]
    connect_code: str
    is_active: bool = True


class HomeworkModel(BaseModel):
    title: str
    file: str
    student_group: Link[StudentGroupModel]
    uploaded_at: datetime
    deadline: datetime
    last_updated_at: datetime
    points: List[float]
    mark_formula: str
    is_active: bool = True


class SubmissionModel(BaseModel):
    student: Link[UserModel]
    homework: Link[HomeworkModel]
    points: List[float]
    fine: float
    mark: float
    start_submit: datetime
    last_updated_at: datetime
    is_active: bool = True


__db_models__ = [UserModel, StudentGroupModel, HomeworkModel, SubmissionModel]