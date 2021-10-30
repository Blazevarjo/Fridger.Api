from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models

from fridger.fridges.models import Fridge
from fridger.shopping_lists.models import ShoppingList
from fridger.utils.enums import (
    FridgeProductStatus,
    QuantityType,
    ShoppingListProductStatus,
)
from fridger.utils.models import BaseModel

User = get_user_model()


class Product(BaseModel):
    name = models.CharField(max_length=60)
    barcode = models.CharField(max_length=100, blank=True)
    image = models.ImageField(blank=True)


class Nutrition(BaseModel):
    product = models.ForeignKey(Product, related_name="nutrition", on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    value = models.FloatField()


class FridgeProduct(BaseModel):
    product = models.ForeignKey(Product, related_name="fridge_product", on_delete=models.CASCADE)
    fridge = models.ForeignKey(Fridge, related_name="fridge_product", on_delete=models.CASCADE)
    expiration_date = models.DateField(blank=True, null=True)
    quantity_type = models.IntegerField(choices=QuantityType.choices)

    @property
    def quantity_base(self) -> Decimal:
        pass

    @property
    def quantity_left(self) -> Decimal:
        pass

    @property
    def quantity_used(self) -> Decimal:
        pass

    @property
    def quantity_wasted(self) -> Decimal:
        pass

    @property
    def quantity_type(self) -> QuantityType:
        pass

    @property
    def sum_price(self) -> Decimal:
        pass


class FridgeProductHistory(BaseModel):
    product = models.ForeignKey(FridgeProduct, related_name="fridge_product_history", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="fridge_product_history", on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=FridgeProductStatus.choices, default=FridgeProductStatus.UNTRACKED)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    qauntity = models.DecimalField(max_digits=10, decimal_places=3)
    quantity_type = models.IntegerField(choices=QuantityType.choices)


class ShoppingListProduct(BaseModel):
    product = models.ForeignKey(Product, related_name="shopping_list_product", on_delete=models.CASCADE)
    shopping_list = models.ForeignKey(ShoppingList, related_name="shopping_list_product", on_delete=models.CASCADE)

    @property
    def quantity_bought(self) -> Decimal:
        pass

    @property
    def quantity_left(self) -> Decimal:
        pass

    @property
    def quantity_type(self) -> QuantityType:
        pass

    @property
    def sum_price(self) -> Decimal:
        pass


class ShoppingListProductHistory(BaseModel):
    product = models.ForeignKey(Product, related_name="shopping_list_product_history", on_delete=models.CASCADE)
    shopping_list = models.ForeignKey(
        ShoppingList, related_name="shopping_list_product_history", on_delete=models.CASCADE
    )
    status = models.IntegerField(choices=ShoppingListProductStatus.choices, default=ShoppingListProductStatus.CREATOR)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    qauntity = models.DecimalField(max_digits=10, decimal_places=3)
    quantity_type = models.CharField(max_length=30)
