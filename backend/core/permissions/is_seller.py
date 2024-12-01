from rest_framework.permissions import BasePermission


class IsUserSeller(BasePermission):

    def has_permission(self, request, view):

        if not request.user:
            return False

        return bool(request.user
                    and request.user.is_seller
                    and request.user.is_active)
