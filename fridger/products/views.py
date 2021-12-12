from rest_framework import viewsets

from fridger.products.models import FridgeProduct, FridgeProductHistory
from fridger.products.serializers import (
    CreateFridgeProductHistorySerializer,
    CreateFridgeProductSerializer,
    UpdateFridgeProductHistorySerializer,
    UpdateFridgeProductSerializer,
)


class FridgeProductViewSet(viewsets.ModelViewSet):
    http_method_names = ("post", "patch", "delete")
    queryset = FridgeProduct.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateFridgeProductSerializer
        elif self.action == "partial_update":
            return UpdateFridgeProductSerializer
        return super().get_serializer_class()


class FridgeProductHistoryViewSet(viewsets.ModelViewSet):
    http_method_names = ("post", "patch", "delete")
    queryset = FridgeProductHistory.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateFridgeProductHistorySerializer
        elif self.action == "partial_update":
            return UpdateFridgeProductHistorySerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
