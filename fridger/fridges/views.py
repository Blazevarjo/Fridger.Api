from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fridger.fridges.models import Fridge, FridgeOwnership
from fridger.fridges.serializers import (
    CreateFridgeOwnershipSerializer,
    FridgeDetailSerializer,
    FridgeOwnershipSerializer,
    FridgeSerializer,
)


class FridgeViewSet(viewsets.ModelViewSet):
    http_method_names = ["post", "get", "put", "delete"]

    queryset = Fridge.objects.none()
    serializer_class = FridgeSerializer

    def get_queryset(self):
        user = self.request.user
        return Fridge.objects.user_fridges(user)

    def get_serializer_class(self):
        if self.action in "retrieve":
            return FridgeDetailSerializer
        if self.action in "ownerships":
            return FridgeOwnershipSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=["get"])
    def ownerships(self, request, pk=None):
        fridge = self.get_object()
        ownerships = fridge.fridge_ownership

        serializer = self.get_serializer(ownerships, many=True)
        return Response(serializer.data)


class FridgeOwnershipViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    http_method_names = ["post", "put", "delete"]

    queryset = FridgeOwnership.objects.none()
    serializer_class = CreateFridgeOwnershipSerializer

    def get_queryset(self):
        user = self.request.user
        return FridgeOwnership.objects.user_fridge_ownerships(user)
