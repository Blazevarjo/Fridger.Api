import django_filters
from django_filters import rest_framework as filters

from fridger.utils.enums import ShoppingListProductStatus

from .models import FridgeProduct


class FridgeProductFilter(filters.FilterSet):
    fridge = django_filters.UUIDFilter(field_name="fridge", required=True)

    class Meta:
        model = FridgeProduct
        fields = ("fridge",)


class ShoppingListProductFilter(filters.FilterSet):
    shopping_list = django_filters.UUIDFilter(field_name="shopping_list", required=True)
    status = django_filters.ChoiceFilter(field_name="status", choices=ShoppingListProductStatus.choices)
