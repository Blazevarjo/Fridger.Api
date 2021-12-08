from rest_framework import serializers

from fridger.fridges.models import Fridge, FridgeOwnership
from fridger.products.serializers import ListFridgeProductSerializer
from fridger.utils.enums import UserPermission


class FridgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fridge
        fields = [
            "id",
            "name",
            "shared_with_count",
            "products_count",
        ]
        read_only_fields = [
            "id",
            "shared_with_count",
            "products_count",
        ]

    def create(self, validated_data):
        user = self.context.get("request").user
        fridge = Fridge.objects.create(**validated_data)
        FridgeOwnership.objects.create(user=user, fridge=fridge, permission=UserPermission.ADMIN)
        return fridge


class FridgeDetailSerializer(serializers.ModelSerializer):
    products = ListFridgeProductSerializer(many=True)

    class Meta:
        model = Fridge
        fields = [
            "id",
            "name",
            "shared_with_count",
            "products_count",
            "products",
        ]
        read_only_fields = fields
