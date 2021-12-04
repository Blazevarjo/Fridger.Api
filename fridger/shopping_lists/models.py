from django.contrib.auth import get_user_model
from django.db import models

from fridger.fridges.models import Fridge
from fridger.shopping_lists.managers import ShoppingListQuerySet
from fridger.utils.models import BaseModel

User = get_user_model()


class ShoppingList(BaseModel):
    # fridge = models.ForeignKey(Fridge, related_name="shopping_list", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=60, blank=True)

    objects = ShoppingListQuerySet.as_manager()


class ShoppingListOwnership(BaseModel):
    class Ownership(models.IntegerChoices):
        ADMIN = 1
        WRITE = 2
        READ = 3

    user = models.ForeignKey(User, related_name="shopping_list_ownership", on_delete=models.RESTRICT)
    shopping_list = models.ForeignKey(ShoppingList, related_name="shopping_list_ownership", on_delete=models.CASCADE)
    ownership = models.IntegerField(choices=Ownership.choices, default=Ownership.READ)


class ShoppingListStatus(BaseModel):
    shopping_list = models.ForeignKey(ShoppingList, related_name="shopping_list_status", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="shopping_list_status", on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
