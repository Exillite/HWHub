from sqlalchemy import Column, DateTime, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from .database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    role = Column(String)
    name = Column(String)
    surname = Column(String)
    patronymic = Column(String)
    email = Column(String)
    vk_id = Column(Integer)
    telegram_id = Column(Integer)
    is_active = Column(Boolean)

    students_groups = relationship("StudentGroup", back_populates="user")

class StudentGroup(Base):
    __tablename__ = "student_groups"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    connect_code = Column(String)
    is_active = Column(Boolean)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="students_groups")

class Homework(Base):
    __tablename__ = "homework"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    file = Column(String)
    uploaded_at = Column(DateTime)
    deadline = Column(DateTime)
    last_updated_at = Column(DateTime)
    mark_formula = Column(String)
    is_active = Column(Boolean)

    student_group_id = Column(Integer, ForeignKey("student_groups.id"))
    student_group = relationship("StudentGroup", back_populates="homework")

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True)
    fine = Column(Float)
    mark = Column(Float)
    start_submit = Column(DateTime)
    last_updated_at = Column(DateTime)
    is_active = Column(Boolean)

    student_id = Column(Integer, ForeignKey("users.id"))
    student = relationship("User", back_populates="submissions")

    homework_id = Column(Integer, ForeignKey("homework.id"))
    homework = relationship("Homework", back_populates="submissions")
