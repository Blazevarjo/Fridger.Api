from django.utils.translation import gettext as _
from rest_framework import exceptions, serializers

from fridger.shopping_lists.models import ShoppingListOwnership
from fridger.users.serializers import BasicDisplayUserSerializer
from fridger.utils.enums import ShoppingListProductStatus, UserPermission

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
            "taken_by",
            "status",
            "name",
            "quantity_type",
            "quantity",
            "note",
        )
        read_only_fields = (
            "id",
            "created_at",
            "taken_by",
            "status",
        )

    def validate(self, attrs):
        request_user = self.context.get("request").user
        shopping_list = attrs.get("shopping_list")
        try:
            ownership = request_user.shopping_list_ownership.get(shopping_list=shopping_list)
        except ShoppingListOwnership.DoesNotExist:
            raise exceptions.PermissionDenied(_("User does not belong to this shopping list."))

        if ownership.permission not in [UserPermission.CREATOR, UserPermission.ADMIN, UserPermission.WRITE]:
            raise exceptions.PermissionDenied(_("User does not have permission to add product to this shopping list."))

        return attrs


class PartialUpdateShoppingListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListProduct
        fields = (
            "id",
            "shopping_list",
            "created_at",
            "taken_by",
            "status",
            "name",
            "price",
            "quantity_type",
            "quantity",
            "note",
        )
        read_only_fields = (
            "id",
            "shopping_list",
            "created_at",
            "created_by",
        )

    def update(self, instance, validated_data):
        user = self.context["request"].user
        if validated_data.get("status") == ShoppingListProductStatus.FREE:
            instance.taken_by = None
        else:
            instance.taken_by = user
        return super().update(instance, validated_data)


class UpdatePriceShoppingListProductSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = ShoppingListProduct
        fields = (
            "id",
            "price",
            "status",
            "taken_by",
            "name",
            "price",
            "quantity_type",
            "quantity",
            "note",
        )
        read_only_fields = (
            "taken_by",
            "status",
            "name",
            "quantity_type",
            "quantity",
            "note",
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
            "quantity",
            "note",
        )
        read_only_fields = fields


class ListShoppingListProductSerializer(serializers.ModelSerializer):
    taken_by = BasicDisplayUserSerializer()

    class Meta:
        model = ShoppingListProduct
        fields = (
            "id",
            "taken_by",
            "status",
            "name",
            "price",
            "quantity_type",
            "quantity",
            "note",
        )
        read_only_fields = fields
