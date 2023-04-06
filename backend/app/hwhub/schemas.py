from pydantic import BaseModel 
from typing import List
from typing import Union
import datetime


class User(BaseModel):
    id: str
    login: str
    role: str
    name: str
    surname: str
    patronymic: str
    email: str
    vk_id: Union[str, None] = None
    telegram_id: Union[str, None] = None
    students_groups: list
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class UserInDB(User):
    password: str


class UserCreate(BaseModel):
    login: str
    name: str
    surname: str
    patronymic: str
    email: str
    password: str

class UserLogin(BaseModel):
    login: str
    password: str

class UserUpdate(BaseModel):
    name: str
    surname: str
    patronymic: str


class StudentGroup(BaseModel):
    pk: str
    title: str
    teacher_id: str
    connect_code: str
    is_active: bool

class StudentGroupCreate(BaseModel):
    title: str
    teacher_id: str

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
    student_group_id: str
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
    
class SubmissionCreate(BaseModel):
    student_id: str
    homework_id: str

class SubmissionUpdate(BaseModel):
    points: List[float]
    fine: float
