from rest_framework.permissions import BasePermission

from .is_superuser_permission import IsSuperUser


class IsSuperUserOrIsStaff(BasePermission):
    def has_permission(self, request, view):
        if not request.user:
            return False

        return bool(IsSuperUser().has_permission(request, view)
                or
                request.user.is_staff and request.user.is_active)
