from rest_framework import serializers

from fridger.products.models import FridgeProduct, FridgeProductHistory


class NestedFridgeProductHistory(serializers.ModelSerializer):
    class Meta:
        model = FridgeProductHistory
        fields = (
            "id",
            "created_by",
            "status",
            "created_at",
            "quantity",
        )
        read_only_fields = (
            "created_at",
            "created_by",
        )


class CreateFridgeProductSerializer(serializers.ModelSerializer):
    product_history = NestedFridgeProductHistory(write_only=True)

    class Meta:
        model = FridgeProduct
        fields = (
            "id",
            "name",
            "producer_name",
            "barcode",
            "image",
            "fridge",
            "expiration_date",
            "quantity_type",
            "product_history",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        product_history = validated_data.pop("product_history")
        product = FridgeProduct.objects.create(**validated_data)
        FridgeProductHistory.objects.create(product=product, created_by=user, **product_history)
        return product


class PartialUpdateFridgeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeProduct
        fields = (
            "id",
            "name",
            "producer_name",
            "image",
            "barcode",
            "expiration_date",
            "quantity_type",
            "quantity_base",
            "quantity_left",
        )
        read_only_fields = (
            "id",
            "quantity_type",
            "quantity_base",
            "quantity_left",
        )


class ListFridgeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeProduct
        fields = (
            "id",
            "name",
            "producer_name",
            "image",
            "barcode",
            "expiration_date",
            "quantity_type",
            "quantity_base",
            "quantity_left",
        )
        read_only_fields = fields


class CreateFridgeProductHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeProductHistory
        fields = (
            "id",
            "created_by",
            "product",
            "status",
            "created_at",
            "quantity",
        )
        read_only_fields = (
            "id",
            "created_at",
            "created_by",
        )


class UpdateFridgeProductHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeProductHistory
        fields = (
            "id",
            "created_by",
            "product",
            "status",
            "created_at",
            "quantity",
        )
        read_only_fields = (
            "id",
            "created_at",
            "created_by",
            "product",
        )
