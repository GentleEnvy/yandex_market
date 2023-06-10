from app.base.permissions.base import BasePermission


class SuperuserPermission(BasePermission):
    requires_authentication = True
    _allow_super = True

    def _has_permission(self, view):
        return False

    def _has_object_permission(self, view, obj):
        return False
