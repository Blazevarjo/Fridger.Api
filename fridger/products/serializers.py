from django.core.exceptions import ValidationError
from rest_framework import serializers

from fridger.products.models import FridgeProduct, FridgeProductHistory


class NestedFridgeProductHistory(serializers.ModelSerializer):
    class Meta:
        model = FridgeProductHistory
        fields = [
            "created_by",
            "status",
            "price",
            "created_at",
            "quantity",
        ]
        read_only_fields = [
            "created_at",
            "status",
        ]


class CreateFridgeProductSerializer(serializers.ModelSerializer):
    product_history = NestedFridgeProductHistory()

    class Meta:
        model = FridgeProduct
        fields = [
            "id",
            "name",
            "barcode",
            "image",
            "fridge",
            "expiration_date",
            "quantity_type",
            "product_history",
        ]

    def create(self, validated_data):
        product_history = validated_data.pop("product_history")
        product = super().create(**validated_data)
        FridgeProductHistory.objects.create(product=product, **product_history)
        return product


class ListFridgeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeProduct
        fields = [
            "id",
            "name",
            "image",
            "expiration_date",
            "quantity_type",
            "quantity_base",
            "quantity_left",
        ]
        read_only_fields = fields
