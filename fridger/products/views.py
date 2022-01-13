from django_filters import rest_framework as django_filters
from rest_framework import filters, mixins, viewsets

from .filters import FridgeProductFilter
from .models import FridgeProduct, FridgeProductHistory, ShoppingListProduct
from .permissions import (
    HasFridgeProductWritePermissions,
    HasShoppingListProductWritePermissions,
)
from .serializers import (
    CreateFridgeProductHistorySerializer,
    CreateFridgeProductSerializer,
    CreateShoppingListProductSerializer,
    ListFridgeProductSerializer,
    ListShoppingListProductSerializer,
    PartialUpdateFridgeProductSerializer,
    PartialUpdateShoppingListProductSerializer,
)

###################
# FRIDGE PRODUCTS #
###################


class FridgeProductViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    http_method_names = ("get", "post", "patch", "delete")
    queryset = FridgeProduct.objects.all()

    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = FridgeProductFilter
    ordering_fields = [
        "name",
        "producer_name",
        "expiration_date",
    ]

    def get_queryset(self):
        if self.action == "list":
            return FridgeProduct.objects.filter(is_available=True).order_by("-created_at")
        return super().get_queryset()

    def filter_queryset(self, queryset):
        if self.action != "list":
            self.filterset_class = None
        return super().filter_queryset(queryset)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateFridgeProductSerializer
        elif self.action == "partial_update":
            return PartialUpdateFridgeProductSerializer
        elif self.action == "list":
            return ListFridgeProductSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ["partial_update", "destroy"]:
            permission_classes = [HasFridgeProductWritePermissions]
        return [permission() for permission in permission_classes]


class FridgeProductHistoryViewSet(viewsets.ModelViewSet):
    http_method_names = ("post",)
    queryset = FridgeProductHistory.objects.all()
    serializer_class = CreateFridgeProductHistorySerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


###########################
# SHOPPING LISTS PRODUCTS #
###########################


class ShoppingListProductViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    http_method_names = ("post", "patch", "delete")
    queryset = ShoppingListProduct.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateShoppingListProductSerializer
        elif self.action == "partial_update":
            return PartialUpdateShoppingListProductSerializer
        elif self.action == "list":
            return ListShoppingListProductSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ["partial_update", "destroy"]:
            permission_classes = [HasShoppingListProductWritePermissions]
        return [permission() for permission in permission_classes]
