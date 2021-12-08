from django.contrib.auth import get_user_model
from django.db import models

from fridger.shopping_lists.managers import ShoppingListQuerySet
from fridger.utils.enums import UserPermission
from fridger.utils.models import BaseModel

User = get_user_model()


class ShoppingList(BaseModel):
    name = models.CharField(max_length=60, blank=True)

    objects = ShoppingListQuerySet.as_manager()


class ShoppingListOwnership(BaseModel):
    user = models.ForeignKey(User, related_name="shopping_list_ownership", on_delete=models.CASCADE)
    shopping_list = models.ForeignKey(ShoppingList, related_name="shopping_list_ownership", on_delete=models.CASCADE)
    ownership = models.IntegerField(choices=UserPermission.choices, default=UserPermission.READ)


class ShoppingListStatus(BaseModel):
    shopping_list = models.ForeignKey(ShoppingList, related_name="shopping_list_status", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="shopping_list_status", on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
