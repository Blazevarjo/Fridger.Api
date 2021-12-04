from django.db import models

from fridger.utils.enums import UserPermission


class ShoppingListQuerySet(models.QuerySet):
    def user_fridges(self, user):
        return self.filter(fridge_ownership__user=user)

    def create_with_permission(self, user, **obj_data):
        shopping_list = super().create(**obj_data)
        shopping_list.shopping_list_ownership.create(user=user, permission=UserPermission.ADMIN)
        return shopping_list
