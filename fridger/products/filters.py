import django_filters
from django_filters import rest_framework as filters

from .models import FridgeProduct


class FridgeProductFilter(filters.FilterSet):
    fridge = django_filters.UUIDFilter(field_name="fridge", required=True)

    class Meta:
        model = FridgeProduct
        fields = ("fridge",)
