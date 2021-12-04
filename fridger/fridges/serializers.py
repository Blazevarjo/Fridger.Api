from rest_framework import serializers

from fridger.fridges.models import Fridge
from fridger.products.serializers import ListFridgeProductSerializer


class FridgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fridge
        fields = [
            "id",
            "name",
            "shared_with_count",
            "products_count",
        ]
        read_only_fields = ["id", "name"]

    def create(self, validated_data):
        user = self.context.get("request").user
        return Fridge.objects.create_with_permission(user, **validated_data)


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
