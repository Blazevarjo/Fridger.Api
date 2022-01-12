from rest_framework import permissions

from fridger.utils.enums import UserPermission

from .models import FridgeOwnership


class IsFrigeAdminOrCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            ownership = obj.fridge_ownership.get(user=request.user)
        except FridgeOwnership.DoesNotExist:
            return False
        return ownership.permission in [UserPermission.ADMIN, UserPermission.CREATOR]


class IsOwnershipCurrentUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsOwnershipAdminOrCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            ownership = FridgeOwnership.objects.get(user=request.user, fridge=obj.fridge)
        except FridgeOwnership.DoesNotExist:
            return False
        return ownership.permission in [UserPermission.ADMIN, UserPermission.CREATOR]
