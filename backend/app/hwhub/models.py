from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from bson import ObjectId

from db import db


class UserModel(BaseModel):
    id: Optional[str] = None

    password: str
    login: str
    role: str
    name: str
    surname: str
    patronymic: str
    email: EmailStr
    vk_id: Optional[str] = None
    telegram_id: Optional[str] = None
    students_groups: List['StudentGroupModel'] = []
    is_active: bool = True

    @classmethod
    def get_collection_name(cls) -> str:
        return "user"

    def to_json(self, with_ids=False):
        data = {
            'login': self.login,
            'role': self.role,
            'name': self.name,
            'surname': self.surname,
            'patronymic': self.patronymic,
            'email': self.email,
            'is_active': self.is_active
        }

        if self.id:
            data['id'] = self.id

        if self.vk_id:
            data['vk_id'] = self.vk_id
        if self.telegram_id:
            data['telegram_id'] = self.telegram_id

        student_groups = []
        if with_ids:
            for group in self.students_groups:
                student_groups.append(group.id)
        else:
            for group in self.students_groups:
                student_groups.append(group.to_json())

        data['students_groups'] = student_groups

        return data

    @classmethod
    async def document_to_object(cls, document) -> 'UserModel':
        document['id'] = str(document['_id'])
        document.pop('_id')
        student_groups = []
        for group in document['students_groups']:
            student_groups.append(await StudentGroupModel.get(id=group))
        document['students_groups'] = student_groups
        return cls(**document)

    @classmethod
    async def get(cls, **kwargs) -> Optional['UserModel']:
        if 'id' in kwargs:
            kwargs['_id'] = ObjectId(kwargs['id'])
            kwargs.pop('id')
        document = await db.db[cls.get_collection_name()].find_one(kwargs)
        if document:
            return await cls.document_to_object(document)
        return None

    @classmethod
    async def find(cls, **kwargs) -> List['UserModel']:
        if 'id' in kwargs:
            kwargs['_id'] = ObjectId(kwargs['id'])
            kwargs.pop('id')
        documents = await db.db[cls.get_collection_name()].find(kwargs)
        users = []
        for document in documents:
            users.append(await cls.document_to_object(document))
        return users

    async def create(self):
        new_document = self.to_json()
        new_document['password'] = self.password
        result = await db.db[self.get_collection_name()].insert_one(new_document)
        self.id = str(result.inserted_id)

    async def update(self):
        document = self.to_json(with_ids=True)
        document.pop('id')
        await db.db[self.get_collection_name()].update_one(
            {'_id': ObjectId(self.id)}, {'$set': document})

    async def delete(self):
        await db.db[self.get_collection_name()].delete_one(
            {'_id': ObjectId(self.id)})


class StudentGroupModel(BaseModel):
    id: Optional[str] = None

    title: str
    teacher: UserModel
    connect_code: Optional[str] = None
    is_active: bool = True

    @classmethod
    def get_collection_name(cls) -> str:
        return "student_group"

    def to_json(self, with_ids=False) -> dict:
        data = {
            'title': self.title,
            'teacher': self.teacher.to_json() if not with_ids else self.teacher.id,
            'connect_code': self.connect_code,
            'is_active': self.is_active
        }

        if self.id:
            data['id'] = self.id

        return data

    @classmethod
    async def document_to_object(cls, document) -> 'StudentGroupModel':
        document['id'] = str(document['_id'])
        document.pop('_id')
        document['teacher'] = await UserModel.get(id=document['teacher'])
        return cls(**document)

    @classmethod
    async def get(cls, **kwargs) -> Optional['StudentGroupModel']:
        if 'id' in kwargs:
            kwargs['_id'] = ObjectId(kwargs['id'])
            kwargs.pop('id')
        document = await db.db[cls.get_collection_name()].find_one(kwargs)
        if document:
            return await cls.document_to_object(document)
        return None

    @classmethod
    async def find(cls, **kwargs) -> List['StudentGroupModel']:
        if 'id' in kwargs:
            kwargs['_id'] = ObjectId(kwargs['id'])
            kwargs.pop('id')
        documents = await db.db[cls.get_collection_name()].find(kwargs)
        student_groups = []
        for document in documents:
            student_groups.append(await cls.document_to_object(document))
        return student_groups

    async def create(self):
        new_document = self.to_json()
        result = await db.db[self.get_collection_name()].insert_one(new_document)
        self.id = str(result.inserted_id)

    async def update(self):
        document = self.to_json(with_ids=True)
        document.pop('id')
        await db.db[self.get_collection_name()].update_one(
            {'_id': ObjectId(self.id)}, {'$set': document})

    async def delete(self):
        await db.db[self.get_collection_name()].delete_one(
            {'_id': ObjectId(self.id)})


class HomeworkModel(BaseModel):
    id: Optional[str] = None

    title: str
    files: List[str]
    student_group: StudentGroupModel
    uploaded_at: datetime
    deadline: datetime
    last_updated_at: datetime
    points: List[float]
    mark_formula: str
    is_active: bool = True

    @classmethod
    def get_collection_name(cls) -> str:
        return "homework"

    def to_json(self, with_ids=False) -> dict:
        data = {
            'title': self.title,
            'files': self.files,
            'student_group': self.student_group.to_json() if not with_ids else self.student_group.id,
            'uploaded_at': str(self.uploaded_at),
            'deadline': str(self.deadline),
            'last_updated_at': str(self.last_updated_at),
            'points': self.points,
            'mark_formula': self.mark_formula,
            'is_active': self.is_active
        }

        if self.id:
            data['id'] = self.id

        return data

    @classmethod
    async def document_to_object(cls, document) -> 'HomeworkModel':
        document['id'] = str(document['_id'])
        document.pop('_id')
        document['student_group'] = await StudentGroupModel.get(
            id=document['student_group'])
        return cls(**document)

    @classmethod
    async def get(cls, **kwargs) -> Optional['HomeworkModel']:
        if 'id' in kwargs:
            kwargs['_id'] = ObjectId(kwargs['id'])
            kwargs.pop('id')
        document = await db.db[cls.get_collection_name()].find_one(kwargs)
        if document:
            return await cls.document_to_object(document)
        return None

    @classmethod
    async def find(cls, **kwargs) -> List['HomeworkModel']:
        if 'id' in kwargs:
            kwargs['_id'] = ObjectId(kwargs['id'])
            kwargs.pop('id')
        documents = await db.db[cls.get_collection_name()].find(kwargs)
        homeworks = []
        for document in documents:
            homeworks.append(await cls.document_to_object(document))
        return homeworks

    async def create(self):
        new_document = self.to_json()
        result = await db.db[self.get_collection_name()].insert_one(new_document)
        self.id = str(result.inserted_id)

    async def update(self):
        document = self.to_json(with_ids=True)
        document.pop('id')
        await db.db[self.get_collection_name()].update_one(
            {'_id': ObjectId(self.id)}, {'$set': document})

    async def delete(self):
        await db.db[self.get_collection_name()].delete_one(
            {'_id': ObjectId(self.id)})


class SubmissionModel(BaseModel):
    id: Optional[str] = None

    student: UserModel
    homework: HomeworkModel
    points: List[float]
    fine: float = 0
    mark: float = 0
    start_submit: datetime
    last_updated_at: datetime
    is_active: bool = True

    @classmethod
    def get_collection_name(cls) -> str:
        return "submission"

    def to_json(self, with_ids=False) -> dict:
        data = {
            'student': self.student.to_json() if not with_ids else self.student.id,
            'homework': self.homework.to_json() if not with_ids else self.homework.id,
            'points': self.points,
            'fine': self.fine,
            'mark': self.mark,
            'start_submit': str(self.start_submit),
            'last_updated_at': str(self.last_updated_at),
            'is_active': self.is_active
        }

        if self.id:
            data['id'] = self.id

        return data

    @classmethod
    async def document_to_object(cls, document) -> 'SubmissionModel':
        document['id'] = str(document['_id'])
        document.pop('_id')
        document['student'] = await UserModel.get(id=document['student'])
        document['homework'] = await HomeworkModel.get(id=document['homework'])
        return cls(**document)

    @classmethod
    async def get(cls, **kwargs) -> Optional['SubmissionModel']:
        if 'id' in kwargs:
            kwargs['_id'] = ObjectId(kwargs['id'])
            kwargs.pop('id')
        document = await db.db[cls.get_collection_name()].find_one(kwargs)
        if document:
            return await cls.document_to_object(document)
        return None

    @classmethod
    async def find(cls, **kwargs) -> List['SubmissionModel']:
        if 'id' in kwargs:
            kwargs['_id'] = ObjectId(kwargs['id'])
            kwargs.pop('id')
        documents = await db.db[cls.get_collection_name()].find(kwargs)
        submissions = []
        for document in documents:
            submissions.append(await cls.document_to_object(document))
        return submissions

    async def create(self):
        new_document = self.to_json()
        result = await db.db[self.get_collection_name()].insert_one(new_document)
        self.id = str(result.inserted_id)

    async def update(self):
        document = self.to_json(with_ids=True)
        document.pop('id')
        await db.db[self.get_collection_name()].update_one(
            {'_id': ObjectId(self.id)}, {'$set': document})

    async def delete(self):
        await db.db[self.get_collection_name()].delete_one(
            {'_id': ObjectId(self.id)})


UserModel.update_forward_refs()
StudentGroupModel.update_forward_refs()
HomeworkModel.update_forward_refs()
SubmissionModel.update_forward_refs()
