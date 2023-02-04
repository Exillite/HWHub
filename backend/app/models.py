from mongoengine import Document
from mongoengine.fields import StringField, IntField, ListField, BooleanField, ReferenceField, URLField, DateTimeField, FloatField


class User(Document):
    password = StringField(required=True)
    role = StringField(required=True)
    name = StringField(required=True)
    surname = StringField(required=True)
    patronymic = StringField(required=True)
    email = StringField(required=True)
    vk_id = IntField(default=None)
    telegram_id = IntField(default=None)
    students_groups = ListField(ReferenceField('StudentGroup'))
    is_active = BooleanField(default=True)


class StudentGroup(Document):
    title = StringField(required=True)
    teacher = ReferenceField('User', required=True)
    connect_code = StringField(required=True)
    is_active = BooleanField(default=True)


class Homework(Document):
    title = StringField(required=True)
    file = URLField(required=True)
    student_group = ReferenceField(StudentGroup, required=True)
    uploaded_at = DateTimeField(required=True)
    deadline = DateTimeField(required=True)
    last_updated_at = DateTimeField(required=True)
    points = ListField(FloatField(), required=True)
    mark_formula = StringField(required=True)
    is_active = BooleanField(default=True)


class Submission(Document):
    student = ReferenceField(User, required=True)
    homework = ReferenceField(Homework, required=True)
    points = ListField(FloatField(), required=True)
    fine = FloatField(default=0)
    mark = FloatField()
    start_submit = DateTimeField(required=True)
    last_updated_at = DateTimeField(required=True)
    is_active = BooleanField(default=True)
