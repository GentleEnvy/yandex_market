from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from app.base.models.base import BaseModel
from app.users.managers import UserManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.TextField(unique=True)
    first_name = models.TextField(default='', blank=True)
    last_name = models.TextField(default='', blank=True)
    is_staff = models.BooleanField(default=False)
    telegram_id = models.BigIntegerField(null=True, blank=True, unique=True)

    is_active = True

    objects = UserManager()

    USERNAME_FIELD = 'username'
