from django.urls import path

from .views import *

urlpatterns = [
    path('api/v0_1/user/<int:id>', UserAPIView.as_view()),
]