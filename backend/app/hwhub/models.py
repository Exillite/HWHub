from mongoengine import Document
from mongoengine.fields import StringField, IntField, ListField, BooleanField, ReferenceField, URLField, DateTimeField, FloatField
from . import schemas

class UserModel(Document):
    password = StringField(required=True)
    login = StringField(required=True)
    role = StringField(required=True)
    name = StringField(required=True)
    surname = StringField(required=True)
    patronymic = StringField(required=True)
    email = StringField(required=True)
    vk_id = IntField(default=None)
    telegram_id = IntField(default=None)
    students_groups = ListField(ReferenceField('StudentGroupModel'), null=True, default=None)
    is_active = BooleanField(default=True)
    
    def to_json(self):
        user_dict = {
            'id': str(self.id),
            'login': self.login,
            'role': self.role,
            'name': self.name,
            'surname': self.surname,
            'patronymic': self.patronymic,
            'email': self.email,
            'is_active': self.is_active,
        }
        
        if self.vk_id:
            user_dict['vk_id'] = self.vk_id
        if self.telegram_id:
            user_dict['telegram_id'] = self.telegram_id

        return user_dict


class StudentGroupModel(Document):
    title = StringField(required=True)
    teacher = ReferenceField('UserModel', required=True)
    connect_code = StringField(default=None)
    is_active = BooleanField(default=True)
    
    def to_json(self):
        student_group = {
            'id': str(self.id),
            'title': self.title,
            'teacher': self.teacher.to_json(),
            'connect_code': self.connect_code,
            'is_active': self.is_active,
        }
        
        return student_group


class HomeworkModel(Document):
    title = StringField(required=True)
    file = URLField(required=True)
    student_group = ReferenceField(StudentGroupModel, required=True)
    uploaded_at = DateTimeField(required=True)
    deadline = DateTimeField(required=True)
    last_updated_at = DateTimeField(required=True)
    points = ListField(FloatField(), required=True)
    mark_formula = StringField(required=True)
    is_active = BooleanField(default=True)
    
    def to_json(self):
        homework = {
            'id': str(self.id),
            'title': self.title,
            'file': self.file,
            'student_group': self.student_group.to_json(),
            'uploaded_at': str(self.uploaded_at),
            'deadline': str(self.deadline),
            'last_updated_at': str(self.last_updated_at),
            'points': [float(p) for p in self.points],
            'mark_formula': self.mark_formula,
            'is_active': self.is_active,
        }
        
        return homework


class SubmissionModel(Document):
    student = ReferenceField(UserModel, required=True)
    homework = ReferenceField(HomeworkModel, required=True)
    points = ListField(FloatField(), required=True)
    fine = FloatField(default=0)
    mark = FloatField()
    start_submit = DateTimeField(required=True)
    last_updated_at = DateTimeField(required=True)
    is_active = BooleanField(default=True)
    
    def to_json(self):
        submission = {
            'id': str(self.id),
            'student': self.student.to_json(),
            'homework': self.homework.to_json(),
            'points': self.points,
            'fine': self.fine,
            'mark': self.mark,
            'start_submit': self.start_submit,
            'last_updated_at': self.last_updated_at,
            'is_active': self.is_active,
        }
        
        return submission
