from .models import CustomUser, StudentGroup, Homework, Submission
from django.contrib.auth.models import User, Group
import re

ROLES = ['NONE', 'teacher', 'student', 'admin', 'consultant']

def is_email_valid(email):
    if re.match(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", email):
        return True
    else:
        return False

def is_password_valid(password):
    if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", password):
        return True
    else:
        return False


class CustomUserModel():
    def __init__(self, id: int):
        if CustomUser.objects.filter(id=id).exists():
            custom_user = CustomUser.objects.get(id=id)
            self.id = custom_user.pk
            self.role = custom_user.user.groups.first().name
            self.name = custom_user.name
            self.surname = custom_user.surname
            self.patronymic = custom_user.patronymic
            self.email = custom_user.email
            self.vk_id = custom_user.vk_id
            self.telegram_id = custom_user.telegram_id
            self.students_groups = []
            for group in custom_user.students_groups.all():
                self.students_groups.append(group.pk)
            self.status_code = 100


        else:
            self.status_code = 201

    def __init__(self, user: CustomUser):
        self.id = user.id
        self.role = user.user.groups.first().name
        self.name = user.name
        self.surname = user.surname
        self.patronymic = user.patronymic
        self.email = user.email
        self.vk_id = user.vk_id
        self.telegram_id = user.telegram_id
        self.students_groups = user.students_groups
        self.status_code = 100
    
    def __init__(self, name, surname, patronymic, email, password):
        custom_user = CustomUser()
        custom_user.name = str(name)
        custom_user.surname = str(surname)
        custom_user.patronymic = str(patronymic)
        
        if is_email_valid(email):
            # check if not exists custom user with this email
            if not CustomUser.objects.filter(email=email).exists():
                custom_user.email = email
            else:
                self.status_code = 201
                return
        else:
            self.status_code = 202
            return
        
        if is_password_valid(password):
            custom_user.user = User.objects.create_user(username=email, password=password)
        else:
            self.status_code = 203
            return

        custom_user.vk_id = None
        custom_user.telegram_id = None
        custom_user.is_active = True

        custom_user.save()
        if not Group.objects.filter(name='student').exists():
            self.status_code = 300
            return
        student_group = Group.objects.get(pk=2)
        custom_user.user.groups.add(student_group)

        custom_user.save()

        self.id = custom_user.pk
        self.role = custom_user.user.groups.first().name
        self.name = custom_user.name
        self.surname = custom_user.surname
        self.patronymic = custom_user.patronymic
        self.email = custom_user.email
        self.vk_id = custom_user.vk_id
        self.telegram_id = custom_user.telegram_id
        self.students_groups = list(custom_user.students_groups.all())
        self.status_code = 100

    def to_dict(self) -> dict:
        data = {
            'id': self.id,
            'role': self.role,
            'name': self.name,
            'surname': self.surname,
            'patronymic': self.patronymic,
            'email': self.email,
            'vk_id': self.vk_id,
            'telegram_id': self.telegram_id,
            'students_groups': self.students_groups
        }
        return data

    def edit(self, name: str, surname: str, patronymic: str) -> int:
        if CustomUser.objects.filter(id=self.id).exists():
            custom_user = CustomUser.objects.get(id=self.id)
            custom_user.name = str(name)
            self.name = str(name)
            custom_user.surname = str(surname)
            self.surname = str(surname)
            custom_user.patronymic = str(patronymic)
            self.patronymic = str(patronymic)
            custom_user.save()
            return custom_user.pk
        else:
            return -1

