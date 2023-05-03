from pydantic import BaseModel, EmailStr
from typing import List
from typing import Union
from datetime import datetime
from typing import Optional
from beanie import PydanticObjectId


class User(BaseModel):
    id: PydanticObjectId
    login: str
    role: str
    name: str
    surname: str
    patronymic: str
    email: EmailStr
    vk_id: Optional[str] = None
    telegram_id: Optional[str] = None
    students_groups: list
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class UserInDB(User):
    password: str


class UserCreate(BaseModel):
    login: str
    name: str
    surname: str
    patronymic: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    login: str
    password: str


class UserUpdate(BaseModel):
    name: str
    surname: str
    patronymic: str


class StudentGroup(BaseModel):
    id: PydanticObjectId
    title: str
    teacher_id: PydanticObjectId
    connect_code: str
    is_active: bool


class StudentGroupCreate(BaseModel):
    title: str
    teacher_id: PydanticObjectId


class StudentGroupUpdate(BaseModel):
    title: str


class Homework(BaseModel):
    id: str
    title: str
    file: List[str]
    student_group: StudentGroup
    uploaded_at: datetime
    deadline: datetime
    last_updated_at: datetime
    points: List[float]
    mark_formula: str
    is_active: bool


class HomeworkCreate(BaseModel):
    title: str
    file: List[str]
    student_group_id: PydanticObjectId
    deadline: datetime
    points: List[float]
    mark_formula: str


class HomeworkUpdate(BaseModel):
    title: str
    file: str
    deadline: datetime
    points: List[float]
    mark_formula: str


class Submission(BaseModel):
    id: str
    student: User
    homework: Homework
    points: List[float]
    fine: float
    mark: float
    start_submit: datetime
    last_updated_at: datetime
    is_active: bool


class SubmissionCreate(BaseModel):
    student_id: PydanticObjectId
    homework_id: PydanticObjectId


class SubmissionUpdate(BaseModel):
    points: List[float]
    fine: float
