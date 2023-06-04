from rest_framework.response import Response

from app.base.views import BaseView
from app.users.serializers.register.telegram import POSTUsersRegisterTelegramSerializer


class UsersRegisterTelegramView(BaseView):
    serializer_map = {'post': POSTUsersRegisterTelegramSerializer}

    def post(self):
        serializer = self.get_valid_serializer()
        user = serializer.save()
        register_verifier.send(user.email)
        return Response(serializer.data, 201)
