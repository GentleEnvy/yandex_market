from app.base.serializers.base import BaseModelSerializer

from app.users.models import User


class POSTUsersRegisterTelegramSerializer(BaseModelSerializer):
    class Meta:
        model = User
        write_only_fields = ['username', 'telegram_id', 'first_name', 'last_name']
        read_only_fields = ['id']
