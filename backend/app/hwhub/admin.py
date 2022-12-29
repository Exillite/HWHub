"""Admin panel for the hwhub app."""
from django.contrib import admin
from .models import StudentGroup, CustomUser, Homework, Submission

admin.site.register(StudentGroup)
admin.site.register(CustomUser)
admin.site.register(Homework)
admin.site.register(Submission)
