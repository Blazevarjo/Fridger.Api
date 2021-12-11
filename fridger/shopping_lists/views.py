from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fridger.shopping_lists.models import ShoppingList, ShoppingListOwnership
from fridger.shopping_lists.serializers import (
    CreateShoppingListOwnershipSerializer,
    PartialUpdateShoppingListOwnershipSerializer,
    ReadOnlyShoppingListOwnershipSerializer,
    ShoppingListSerializer,
)


class ShoppingListViewSet(viewsets.ModelViewSet):
    http_method_names = ["post", "get", "patch", "delete"]

    queryset = ShoppingList.objects.none()
    serializer_class = ShoppingListSerializer

    def get_queryset(self):
        user = self.request.user
        return ShoppingList.objects.user_shopping_lists(user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ShoppingListSerializer
        if self.action == "ownerships":
            return ReadOnlyShoppingListOwnershipSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=["get"])
    def ownerships(self, request, pk=None):
        shopping_list = self.get_object()
        ownerships = shopping_list.shopping_list_ownership

        serializer = self.get_serializer(ownerships, many=True)
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
