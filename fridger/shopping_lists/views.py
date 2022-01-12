from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fridger.products.serializers import ListShoppingListProductSerializer

from .models import ShoppingList, ShoppingListOwnership
from .permissions import (
    IsOwnershipAdminOrCreator,
    IsOwnershipCurrentUser,
    IsShoppingListAdminOrCreator,
)
from .serializers import (
    BuyListOfProductsSerializer,
    CreateShoppingListOwnershipSerializer,
    CreateShoppingListSerializer,
    DetailShoppingListSerializer,
    ListShoppingListSerializer,
    PartialUpdateShoppingListOwnershipSerializer,
    PartialUpdateShoppingListSerializer,
    ReadOnlyShoppingListOwnershipSerializer,
    ReadOnlySummaryProducts,
    ReadOnlyYourProductsSerializer,
)


class ShoppingListViewSet(viewsets.ModelViewSet):
    http_method_names = ["post", "get", "patch", "delete"]

    queryset = ShoppingList.objects.none()
    serializer_class = DetailShoppingListSerializer
    filterset_fields = ["is_archived"]

    def get_queryset(self):
        user = self.request.user
        if self.action == "all_products":
            return (
                ShoppingList.objects.user_shopping_lists(user)
                .prefetch_related("shopping_list_product__taken_by")
                .order_by("-created_at")
            )
        return ShoppingList.objects.user_shopping_lists(user).order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DetailShoppingListSerializer
        if self.action == "list":
            return ListShoppingListSerializer
        if self.action == "create":
            return CreateShoppingListSerializer
        if self.action == "partial_update":
            return PartialUpdateShoppingListSerializer
        if self.action == "ownerships":
            return ReadOnlyShoppingListOwnershipSerializer
        if self.action == "buy_products":
            return BuyListOfProductsSerializer
        if self.action == "all_products":
            return ListShoppingListProductSerializer
        if self.action == "your_products":
            return ReadOnlyYourProductsSerializer
        if self.action == "summary":
            return ReadOnlySummaryProducts
        return super().get_serializer_class()

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ["partial_update", "destroy"]:
            permission_classes = [IsShoppingListAdminOrCreator]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["get"])
    def ownerships(self, request, pk=None):
        shopping_list = self.get_object()
        ownerships = shopping_list.shopping_list_ownership

        serializer = self.get_serializer(ownerships, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="buy-products")
    def buy_products(self, request, pk=None):
        shopping_list = self.get_object()
        serializer = self.get_serializer(shopping_list, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    @action(detail=True, methods=["get"], url_path="all-products")
    def all_products(self, request, pk=None):
        shopping_list = self.get_object()
        products = shopping_list.shopping_list_product.order_by("-updated_at")

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="your-products")
    def your_products(self, request, pk=None):
        shopping_list = self.get_object()
        serializer = self.get_serializer(shopping_list)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def summary(self, request, pk=None):
        shopping_list = self.get_object()
        serializer = self.get_serializer(shopping_list)
        return Response(serializer.data)


class ShoppingListOwnershipViewSet(viewsets.ModelViewSet):
    http_method_names = ["post", "patch", "delete"]

    queryset = ShoppingListOwnership.objects.none()
    serializer_class = CreateShoppingListOwnershipSerializer

    def get_queryset(self):
        user = self.request.user
        return ShoppingListOwnership.objects.user_shopping_list_ownerships(user)

    def get_serializer_class(self):
        if self.action == "partial_update":
            return PartialUpdateShoppingListOwnershipSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action == "partial_update":
            permission_classes = [IsOwnershipAdminOrCreator]
        if self.action == "destroy":
            permission_classes = [IsOwnershipCurrentUser | IsOwnershipAdminOrCreator]
        return [permission() for permission in permission_classes]
