from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Fridge, FridgeOwnership
from .permissions import (
    IsFrigeAdminOrCreator,
    IsOwnershipAdminOrCreator,
    IsOwnershipCurrentUser,
)
from .serializers import (
    CreateFridgeOwnershipSerializer,
    FridgeDetailSerializer,
    FridgeSerializer,
    PartialUpdateFridgeOwnershipSerializer,
    ReadOnlyFridgeOwnershipSerializer,
)


class FridgeViewSet(viewsets.ModelViewSet):
    http_method_names = ["post", "get", "put", "delete"]

    queryset = Fridge.objects.none()
    serializer_class = FridgeSerializer

    def get_queryset(self):
        user = self.request.user
        return Fridge.objects.user_fridges(user).order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FridgeDetailSerializer
        if self.action == "ownerships":
            return ReadOnlyFridgeOwnershipSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ["update", "destroy"]:
            permission_classes = [IsFrigeAdminOrCreator]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["get"])
    def ownerships(self, request, pk=None):
        fridge = self.get_object()
        ownerships = fridge.fridge_ownership

        serializer = self.get_serializer(ownerships, many=True)
        return Response(serializer.data)


class FridgeOwnershipViewSet(viewsets.ModelViewSet):
    http_method_names = ["post", "patch", "delete"]

    queryset = FridgeOwnership.objects.none()
    serializer_class = CreateFridgeOwnershipSerializer

    def get_queryset(self):
        user = self.request.user
        return FridgeOwnership.objects.user_fridge_ownerships(user)

    def get_serializer_class(self):
        if self.action == "partial_update":
            return PartialUpdateFridgeOwnershipSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action == "partial_update":
            permission_classes = [IsOwnershipAdminOrCreator]
        if self.action == "destroy":
            permission_classes = [IsOwnershipCurrentUser | IsOwnershipAdminOrCreator]
        return [permission() for permission in permission_classes]
