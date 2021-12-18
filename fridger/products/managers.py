from django.db import models
from django.db.models import Q
from django.db.models.aggregates import Sum

from fridger.utils.enums import FridgeProductStatus, ShoppingListProductStatus


class FridgeProductHistoryQuerySet(models.QuerySet):
    def quantities(self):
        return self.aggregate(
            quantity_base=Sum("quantity", filter=Q(status=FridgeProductStatus.UNUSED)),
            quantity_used=Sum("quantity", filter=Q(status=FridgeProductStatus.USED)),
            quantity_wasted=Sum("quantity", filter=Q(status=FridgeProductStatus.WASTED)),
        )


class ShoppingListProductHistoryQuerySet(models.QuerySet):
    def quantities(self):
        return self.aggregate(
            quantity_base=Sum("quantity", filter=Q(status=ShoppingListProductStatus.FREE)),
            quantity_bought=Sum("quantity", filter=Q(status=ShoppingListProductStatus.BUYER)),
        )

    def price_sum(self):
        return self.aggregate(price_sum=Sum("price"))
