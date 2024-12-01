from rest_framework.permissions import BasePermission

from .is_seller import IsUserSeller


class IsSellerPremium(BasePermission):

    def has_permission(self, request, view):

        if not request.user:
            return False

        return bool(IsUserSeller().has_permission(request, view)
                    and
                    request.user.is_premium)
