from app.base.serializers.base import BaseModelSerializer

from app.users.models import User


class GETUsersMeSerializer(BaseModelSerializer):
    class Meta:
        model = User
        read_only_fields = ['id', 'username', 'telegram_id', 'first_name', 'last_name']
