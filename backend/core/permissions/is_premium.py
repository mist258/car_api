from rest_framework.permissions import BasePermission


class IsUserPremium(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user
                    and request.user.is_premium
                    and request.user.is_seller
                    and request.user.is_active)
