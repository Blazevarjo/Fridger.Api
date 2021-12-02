from rest_framework import viewsets

from fridger.fridges.models import Fridge
from fridger.fridges.serializers import CreateOrUpdateFridgeSerializer


class FridgeViewSet(viewsets.ModelViewSet):
    queryset = Fridge.objects.none()
    http_method_names = ["post", "get", "put", "delete"]

    def get_queryset(self):
        user = self.request.user
        return Fridge.objects.user_fridges(user)

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return CreateOrUpdateFridgeSerializer
        return super().get_serializer_class()
