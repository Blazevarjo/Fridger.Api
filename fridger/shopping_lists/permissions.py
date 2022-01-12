from rest_framework import permissions

from fridger.utils.enums import UserPermission

from .models import ShoppingListOwnership


class IsShoppingListAdminOrCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            ownership = obj.shopping_list_ownership.get(user=request.user)
        except ShoppingListOwnership.DoesNotExist:
            return False
        return ownership.permission in [UserPermission.ADMIN, UserPermission.CREATOR]


class IsOwnershipCurrentUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsOwnershipAdminOrCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            ownership = ShoppingListOwnership.objects.get(user=request.user, shopping_list=obj.shopping_list)
        except ShoppingListOwnership.DoesNotExist:
            return False
        return ownership.permission in [UserPermission.ADMIN, UserPermission.CREATOR]
