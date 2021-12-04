from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models

from fridger.fridges.models import Fridge
from fridger.products.managers import (
    FridgeProductHistoryQuerySet,
    ShoppingListProductHistoryQuerySet,
)
from fridger.shopping_lists.models import ShoppingList
from fridger.utils.enums import (
    FridgeProductStatus,
    QuantityType,
    ShoppingListProductStatus,
)
from fridger.utils.models import BaseModel

User = get_user_model()


class FridgeProduct(BaseModel):
    name = models.CharField(max_length=60)
    barcode = models.CharField(max_length=100, blank=True)
    image = models.ImageField(blank=True)

    fridge = models.ForeignKey(Fridge, related_name="fridge_product", on_delete=models.CASCADE)
    expiration_date = models.DateField(blank=True, null=True)
    quantity_type = models.IntegerField(choices=QuantityType.choices)
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

    @property
    def sum_price(self) -> Decimal:
        return self.fridge_product_history.price_sum()["price_sum"] or Decimal(0)


class FridgeProductHistory(BaseModel):
    product = models.ForeignKey(FridgeProduct, related_name="fridge_product_history", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="fridge_product_history", on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=FridgeProductStatus.choices, default=FridgeProductStatus.UNUSED)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)

    objects = FridgeProductHistoryQuerySet.as_manager()

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        product = self.product
        product.is_available = product.quantity_left > 0
        product.save()
        return instance


class ShoppingListProduct(BaseModel):
    name = models.CharField(max_length=60)
    barcode = models.CharField(max_length=100, blank=True)
    image = models.ImageField(blank=True)

    shopping_list = models.ForeignKey(ShoppingList, related_name="shopping_list_product", on_delete=models.CASCADE)
    quantity_type = models.IntegerField(choices=QuantityType.choices)

    @property
    def quantity_base(self) -> Decimal:
        return self.shopping_list_product_history.quantities()["quantity_base"] or Decimal(0)

    @property
    def quantity_bought(self) -> Decimal:
        return self.shopping_list_product_history.quantities()["quantity_bought"] or Decimal(0)

    @property
    def quantity_left(self) -> Decimal:
        return self.quantity_base - self.quantity_bought

    @property
    def sum_price(self) -> Decimal:
        return self.shopping_list_product_history.price_sum()["price_sum"] or Decimal(0)


class ShoppingListProductHistory(BaseModel):
    product = models.ForeignKey(
        ShoppingListProduct, related_name="shopping_list_product_history", on_delete=models.CASCADE
    )
    shopping_list = models.ForeignKey(
        ShoppingList, related_name="shopping_list_product_history", on_delete=models.CASCADE
    )
    status = models.IntegerField(choices=ShoppingListProductStatus.choices, default=ShoppingListProductStatus.CREATOR)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    qauntity = models.DecimalField(max_digits=10, decimal_places=3)

    objects = ShoppingListProductHistoryQuerySet.as_manager()
