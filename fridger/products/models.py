from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models

from fridger.fridges.models import Fridge
from fridger.products.managers import FridgeProductHistoryQuerySet
from fridger.shopping_lists.models import ShoppingList, ShoppingListFragment
from fridger.utils.enums import (
    FridgeProductStatus,
    QuantityType,
    ShoppingListProductStatus,
)
from fridger.utils.models import BaseModel

User = get_user_model()


class FridgeProduct(BaseModel):
    fridge = models.ForeignKey(Fridge, related_name="fridge_product", on_delete=models.CASCADE)

    name = models.CharField(max_length=60)
    producer_name = models.CharField(max_length=60, blank=True)
    barcode = models.CharField(max_length=100, blank=True)
    image = models.URLField(blank=True)

    expiration_date = models.DateField(blank=True, null=True)
    quantity_type = models.CharField(choices=QuantityType.choices, max_length=5)
    is_available = models.BooleanField(default=True)

    @property
    def quantity_base(self) -> Decimal:
        return self.fridge_product_history.quantities()["quantity_base"] or Decimal(0)

    @property
    def quantity_left(self) -> Decimal:
        return self.quantity_base - self.quantity_used - self.quantity_wasted

    @property
    def quantity_used(self) -> Decimal:
        return self.fridge_product_history.quantities()["quantity_used"] or Decimal(0)

    @property
    def quantity_wasted(self) -> Decimal:
        return self.fridge_product_history.quantities()["quantity_wasted"] or Decimal(0)

    def update_is_available(self):
        self.is_available = self.quantity_left > 0
        self.save()


class FridgeProductHistory(BaseModel):
    product = models.ForeignKey(FridgeProduct, related_name="fridge_product_history", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="fridge_product_history", on_delete=models.SET_NULL, null=True)

    status = models.CharField(choices=FridgeProductStatus.choices, default=FridgeProductStatus.UNUSED, max_length=9)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)

    objects = FridgeProductHistoryQuerySet.as_manager()

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        self.product.update_is_available()
        return instance

    def delete(self, *args, **kwargs):
        instance = super().delete(*args, **kwargs)
        self.product.update_is_available()
        return instance


class ShoppingListProduct(BaseModel):
    class Meta:
        ordering = ["-created_at"]

    shopping_list = models.ForeignKey(ShoppingList, related_name="shopping_list_product", on_delete=models.CASCADE)
    shopping_list_fragment = models.ForeignKey(
        ShoppingListFragment, related_name="shopping_list_product", on_delete=models.CASCADE, blank=True, null=True
    )
    created_by = models.ForeignKey(User, related_name="shopping_list_product", on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=60)
    note = models.TextField(blank=True)

    status = models.CharField(
        choices=ShoppingListProductStatus.choices, default=ShoppingListProductStatus.FREE, max_length=12
    )
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    quantity_type = models.CharField(choices=QuantityType.choices, max_length=5)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        self.shopping_list.update_is_archived()
        return instance

    def delete(self, *args, **kwargs):
        instance = super().delete(*args, **kwargs)
        self.shopping_list.update_is_archived()
        return instance
