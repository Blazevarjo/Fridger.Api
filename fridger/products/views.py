from rest_framework import viewsets

from fridger.products.models import FridgeProduct
from fridger.products.serializers import (
    CreateFridgeProductSerializer,
    ListFridgeProductSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = FridgeProduct.objects.all()

    def get_serializer_class(self):
        if self.action in ["create"]:
            return CreateFridgeProductSerializer
        elif self.action == "list":
            return ListFridgeProductSerializer
        return super().get_serializer_class()
