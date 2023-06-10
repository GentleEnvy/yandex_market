from abc import ABC

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from app.users.models import User


class SecretAuthentication(BaseAuthentication):
    class Admin(AnonymousUser, ABC):
        is_staff = True
        is_active = True
        is_superuser = True

    keyword = 'Secret'

    def __init__(self):
        self.secret = settings.TELEGRAM_SECRET

    def authenticate(self, request):
        if self.secret is None:
            return None
        header = get_authorization_header(request).decode()
        try:
            keyword, secret, telegram_id = header.split()
        except ValueError:
            try:
                keyword, secret = header.split()
            except ValueError:
                return None
            telegram_id = None
        if keyword != self.keyword or secret != self.secret:
            return None
        try:
            if telegram_id:
                return User.objects.get(telegram_id=telegram_id), self.keyword
            return self.Admin, self.keyword
        except User.DoesNotExist:
            return None
