from rest_framework.response import Response

from app.base.views import BaseView
from app.users.models import User
from app.users.serializers.register.telegram import POSTUsersRegisterTelegramSerializer


class UsersRegisterTelegramView(BaseView):
    serializer_map = {'post': POSTUsersRegisterTelegramSerializer}

    def post(self):
        serializer = self.get_valid_serializer()
        serializer.instance = User.objects.filter(
            telegram_id=serializer.validated_data['telegram_id']
        ).first()
        serializer.save()
        return Response(serializer.data, status=201)
