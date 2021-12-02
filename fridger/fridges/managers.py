from django.db import models

from fridger.utils.enums import UserPermission


class FridgeQuerySet(models.QuerySet):
    def user_fridges(self, user):
        return self.filter(fridge_ownership__user=user)

    def create_with_permission(self, user, **obj_data):
        fridge = super().create(**obj_data)
        fridge.fridge_ownership.create(user=user, permission=UserPermission.ADMIN)
        return fridge
