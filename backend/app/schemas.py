from pydantic import BaseModel 
from typing import Optional, List
import datetime

class User(BaseModel):
    pk: str
    role: str
    name: str
    surname: str
    patronymic: str
    email: str
    vk_id: int = None
    telegram_id: int = None
    students_groups: list = None
    is_active: bool

class UserCreate(BaseModel):
    name: str
    surname: str
    patronymic: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    name: str
    surname: str
    patronymic: str


class StudentGroup(BaseModel):
    pk: str
    title: str
    teacher: User
    connect_code: str
    is_active: bool


class StudentGroupCreate(BaseModel):
    title: str
    teacher: User

class StudentGroupUpdate(BaseModel):
    title: str


class Homework(BaseModel):
    pk: str
    title: str
    file: str
    student_group: StudentGroup
    uploaded_at: datetime.datetime
    deadline: datetime.datetime
    last_updated_at: datetime.datetime
    points: List[float]
    mark_formula: str
    is_active: bool

class HomeworkCreate(BaseModel):
    title: str
    file: str
    student_group: StudentGroup
    deadline: datetime.datetime
    points: List[float]
    mark_formula: str

class HomeworkUpdate(BaseModel):
    title: str
    file: str
    deadline: datetime.datetime
    points: List[float]
    mark_formula: str


class Submission(BaseModel):
    pk: str
    student: User
    homework: Homework
    points: List[float]
    fine: float
    mark: float
    start_submit: datetime.datetime
    last_updated_at: datetime.datetime
    is_active: bool
