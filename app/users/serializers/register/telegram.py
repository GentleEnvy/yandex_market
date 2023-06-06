from django.conf import settings
from rest_framework import serializers

from app.base.serializers.base import BaseModelSerializer
from app.users.models import User


class POSTUsersRegisterTelegramSerializer(BaseModelSerializer):
    password = serializers.HiddenField(default=settings.TELEGRAM_SECRET)

    class Meta:
        model = User
        extra_kwargs = {'telegram_id': {'required': True, 'allow_null': False}}
        write_only_fields = [
            'username',
            'telegram_id',
            'first_name',
            'last_name',
            'password',
        ]
        read_only_fields = ['id']
