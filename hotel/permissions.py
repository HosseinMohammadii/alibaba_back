from rest_framework.permissions import BasePermission


class IsHotelOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'OPTIONS':
            return True

        if request.user and request.user.is_authenticated:
            return obj.owner == request.user
        return False


class IsRoomHotelOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'OPTIONS':
            return True

        if request.user and request.user.is_authenticated:
            return obj.hotel.owner == request.user
        return False


class IsFacilityHotelOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'OPTIONS':
            return True

        if request.user and request.user.is_authenticated:
            return obj.hotel.owner == request.user
        return False
