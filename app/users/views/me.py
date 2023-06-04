from app.base.views.base import BaseView
from app.users.permissions import AuthenticatedPermission
from app.users.serializers.me import GETUsersMeSerializer


class UsersMeView(BaseView):
    permissions_map = {'get': [AuthenticatedPermission]}
    serializer_map = {'get': GETUsersMeSerializer}

    def get(self):
        return self.retrieve()

    def get_object(self):
        return self.request.user
