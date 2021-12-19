from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fridger.products.serializers import ListShoppingListProductSerializer

from .models import ShoppingList, ShoppingListFragment, ShoppingListOwnership
from .serializers import (
    CreateShoppingListFragmentSerializer,
    CreateShoppingListOwnershipSerializer,
    PartialUpdateShoppingListOwnershipSerializer,
    PartialUpdateShoppingListSerializer,
    ReadOnlyShoppingListOwnershipSerializer,
    ReadOnlySummaryProducts,
    ReadOnlyYourProductsSerializer,
    ShoppingListSerializer,
)


class ShoppingListViewSet(viewsets.ModelViewSet):
    http_method_names = ["post", "get", "patch", "delete"]

    queryset = ShoppingList.objects.none()
    serializer_class = ShoppingListSerializer
    filterset_fields = ["is_archived"]

    def get_queryset(self):
        user = self.request.user
        if self.action == "all_products":
            return ShoppingList.objects.user_shopping_lists(user).prefetch_related("shopping_list_product__created_by")
        return ShoppingList.objects.user_shopping_lists(user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ShoppingListSerializer
        if self.action == "partial_update":
            return PartialUpdateShoppingListSerializer
        if self.action == "ownerships":
            return ReadOnlyShoppingListOwnershipSerializer
        if self.action == "all_products":
            return ListShoppingListProductSerializer
        if self.action == "your_products":
            return ReadOnlyYourProductsSerializer
        if self.action == "summary":
            return ReadOnlySummaryProducts
        return super().get_serializer_class()

    @action(detail=True, methods=["get"])
    def ownerships(self, request, pk=None):
        shopping_list = self.get_object()
        ownerships = shopping_list.shopping_list_ownership

        serializer = self.get_serializer(ownerships, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def all_products(self, request, pk=None):
        shopping_list = self.get_object()
        products = shopping_list.shopping_list_product

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
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

    def get_serializer_class(self):
        if self.action == "partial_update":
            return PartialUpdateShoppingListOwnershipSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        return ShoppingListOwnership.objects.user_shopping_list_ownerships(user)


class ShoppingListFragmentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    queryset = ShoppingListFragment.objects.none()
    serializer_class = CreateShoppingListFragmentSerializer
