from rest_framework import serializers

from fridger.users.serializers import BasicDisplayUserSerializer

from .models import FridgeProduct, FridgeProductHistory, ShoppingListProduct

###################
# FRIDGE PRODUCTS #
###################


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


###########################
# SHOPPING LISTS PRODUCTS #
###########################


class CreateShoppingListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListProduct
        fields = (
            "id",
            "shopping_list",
            "created_at",
            "created_by",
            "status",
            "name",
            "price",
            "quantity_type",
            "qauntity",
            "note",
        )
        read_only_fields = (
            "id",
            "created_at",
            "created_by",
            "status",
        )


class PartialUpdateShoppingListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListProduct
        fields = (
            "id",
            "shopping_list",
            "created_at",
            "created_by",
            "status",
            "name",
            "price",
            "quantity_type",
            "qauntity",
            "note",
        )
        read_only_fields = (
            "id",
            "shopping_list",
            "created_at",
            "created_by",
        )


class BasicListShoppingListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListProduct
        fields = (
            "id",
            "status",
            "name",
            "price",
            "quantity_type",
            "qauntity",
            "note",
        )
        read_only_fields = fields


class ListShoppingListProductSerializer(serializers.ModelSerializer):
    created_by = BasicDisplayUserSerializer()

    class Meta:
        model = ShoppingListProduct
        fields = (
            "id",
            "created_by",
            "status",
            "name",
            "price",
            "quantity_type",
            "qauntity",
            "note",
        )
        read_only_fields = fields
