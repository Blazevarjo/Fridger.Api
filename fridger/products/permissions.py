from rest_framework import permissions

from fridger.shopping_lists.models import ShoppingListOwnership
from fridger.utils.enums import UserPermission


class HasProductWritePermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            ownership = ShoppingListOwnership.objects.get(user=request.user, shopping_list=obj.shopping_list)
        except ShoppingListOwnership.DoesNotExist:
            return False
        return ownership.permission in [UserPermission.ADMIN, UserPermission.CREATOR] or (
            ownership.permission == UserPermission.WRITE and request.user == obj.user
        )
