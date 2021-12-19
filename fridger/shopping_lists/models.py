from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q

from fridger.fridges.models import Fridge
from fridger.utils.enums import ShoppingListProductStatus, UserPermission
from fridger.utils.models import BaseModel

from .managers import ShoppingListOwnershipQuerySet, ShoppingListQuerySet

User = get_user_model()


class ShoppingList(BaseModel):
    fridge = models.ForeignKey(Fridge, related_name="shopping_list", blank=True, null=True, on_delete=models.SET_NULL)

    name = models.CharField(max_length=60)
    is_archived = models.BooleanField(default=False)

    objects = ShoppingListQuerySet.as_manager()

    @property
    def free_products_count(self) -> int:
        return self.shopping_list_product.filter(status=ShoppingListProductStatus.FREE).count()

    @property
    def taken_products_count(self) -> int:
        return self.shopping_list_product.filter(
            Q(status=ShoppingListProductStatus.TAKER) | Q(status=ShoppingListProductStatus.TAKER_MARKED)
        ).count()

    @property
    def bought_products_count(self) -> int:
        return self.shopping_list_product.filter(status=ShoppingListProductStatus.BUYER).count()

    @property
    def is_shared(self) -> bool:
        return self.shopping_list_ownership.count() > 1

    def update_is_archived(self):
        self.is_archived = self.shopping_list_product.exclude(status=ShoppingListProductStatus.BUYER).count() == 0
        self.save()

    def __str__(self) -> str:
        return self.name


class ShoppingListFragment(BaseModel):
    shopping_list = models.ForeignKey(ShoppingList, related_name="shopping_list_fragment", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="shopping_list_fragment", null=True, on_delete=models.SET_NULL)

    price = models.DecimalField(max_digits=9, decimal_places=2)


class ShoppingListOwnership(BaseModel):
    user = models.ForeignKey(User, related_name="shopping_list_ownership", on_delete=models.CASCADE)
    shopping_list = models.ForeignKey(ShoppingList, related_name="shopping_list_ownership", on_delete=models.CASCADE)

    permission = models.CharField(choices=UserPermission.choices, default=UserPermission.READ, max_length=7)

    objects = ShoppingListOwnershipQuerySet.as_manager()
