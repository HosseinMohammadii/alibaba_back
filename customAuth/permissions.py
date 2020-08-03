from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool((request.user and request.user.is_authenticated) or request.method == 'OPTIONS')


class UserIsHotelOwner(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool((request.user and request.user.is_authenticated and request.user.is_hotel_owner) or request.method == 'OPTIONS')
