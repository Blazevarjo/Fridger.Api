from rest_framework import viewsets

from fridger.fridges.models import Fridge
from fridger.fridges.serializers import FridgeDetailSerializer, FridgeSerializer


class FridgeViewSet(viewsets.ModelViewSet):
    queryset = Fridge.objects.none()
    http_method_names = ["post", "get", "put", "delete"]

    serializer_class = FridgeSerializer

    def get_queryset(self):
        user = self.request.user
        return Fridge.objects.user_fridges(user)

    def get_serializer_class(self):
        if self.action in "retrieve":
            return FridgeDetailSerializer
        return super().get_serializer_class()
