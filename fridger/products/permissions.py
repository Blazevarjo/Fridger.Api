from rest_framework import permissions

from fridger.fridges.models import FridgeOwnership
from fridger.shopping_lists.models import ShoppingListOwnership
from fridger.utils.enums import UserPermission


class HasFridgeProductWritePermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            ownership = FridgeOwnership.objects.get(user=request.user, fridge=obj.fridge)
        except FridgeOwnership.DoesNotExist:
            return False
        return ownership.permission in [UserPermission.ADMIN, UserPermission.CREATOR, UserPermission.WRITE]


class HasShoppingListProductWritePermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            ownership = ShoppingListOwnership.objects.get(user=request.user, shopping_list=obj.shopping_list)
        except ShoppingListOwnership.DoesNotExist:
            return False
        return ownership.permission in [UserPermission.ADMIN, UserPermission.CREATOR, UserPermission.WRITE]
