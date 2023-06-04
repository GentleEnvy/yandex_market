from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from app.users.models import User


class SecretAuthentication(BaseAuthentication):
    keyword = 'Secret'
    
    def __init__(self):
        self.secret = settings.TELEGRAM_SECRET

    def authenticate(self, request):
        if self.secret is None:
            return None
        header = get_authorization_header(request).split()
        try:
            keyword, secret, telegram_id = header.split()
        except TypeError:
            return None
        if keyword != self.keyword or secret != self.secret:
            return None
        try:
            return User.objects.get(telegram_id=telegram_id), self.keyword
        except User.DoesNotExist:
            return None
