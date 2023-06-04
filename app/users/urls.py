from django.urls import path

from .views import (
    UsersMeView,
    UsersRegisterTelegramView,
)

urlpatterns = [
    path('register/telegram/', UsersRegisterTelegramView.as_view()),
    path('me/', UsersMeView.as_view()),
]
