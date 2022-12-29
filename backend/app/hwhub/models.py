from django.db import models


class StudentGroup(models.Model):
    title = models.CharField(max_length=100)
    teacher = models.ForeignKey('CustomUser', on_delete=models.PROTECT)
    connect_code = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField()

    def __str__(self):
        return f"<Group-{self.pk}> {self.title}"


class CustomUser(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    vk_id = models.IntegerField(null=True)
    telegram_id = models.IntegerField(null=True)
    students_groups = models.ManyToManyField(StudentGroup)
    is_active = models.BooleanField()

    def __str__(self):
        return f"<User-{self.pk}> {self.surname} {self.name}"


class Homework(models.Model):
    title = models.CharField(max_length=100)
    file = models.CharField(max_length=100)
    student_group = models.ForeignKey(StudentGroup, on_delete=models.PROTECT)
    uploaded_at = models.DateTimeField()
    deadline = models.DateTimeField()
    last_updated_at = models.DateTimeField()
    points = models.JSONField()
    mark_formula = models.CharField(max_length=100)
    is_active = models.BooleanField()

    def __str__(self):
        return f"<Homework-{self.pk}> {self.title}"


class Submission(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    homework = models.ForeignKey(Homework, on_delete=models.PROTECT)
    points = models.JSONField()
    fine = models.FloatField()
    mark = models.FloatField()
    start_submit = models.DateTimeField()
    last_updated_at = models.DateTimeField()
    is_active = models.BooleanField()

    def __str__(self):
        return f"<Submission-{self.pk}> {self.student} {self.homework}"
