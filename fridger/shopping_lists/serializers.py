from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import Q
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from fridger.products.models import ShoppingListProduct
from fridger.products.serializers import (
    BasicListShoppingListProductSerializer,
    UpdatePriceShoppingListProductSerializer,
)
from fridger.users.serializers import BasicUserSerializer
from fridger.utils.enums import ShoppingListProductStatus, UserPermission

from .models import ShoppingList, ShoppingListOwnership

User = get_user_model()


##################
# SHOPPING LISTS #
##################


class PartialUpdateShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ("name",)


class CurrentUserShoppingListOwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListOwnership
        fields = (
            "id",
            "permission",
        )
        read_only_fields = fields


class ShoppingListSerializer(serializers.ModelSerializer):
    my_ownership = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingList
        fields = (
            "id",
            "fridge",
            "name",
            "free_products_count",
            "taken_products_count",
            "bought_products_count",
            "is_archived",
            "is_shared",
            "my_ownership",
        )
        read_only_fields = (
            "id",
            "free_products_count",
            "taken_products_count",
            "bought_products_count",
            "is_archived",
            "is_shared",
            "my_ownership",
        )

    def create(self, validated_data):
        user = self.context.get("request").user
        shopping_list = ShoppingList.objects.create(**validated_data)
        ShoppingListOwnership.objects.create(user=user, shopping_list=shopping_list, permission=UserPermission.CREATOR)
        return shopping_list

    @extend_schema_field(CurrentUserShoppingListOwnershipSerializer)
    def get_my_ownership(self, obj):
        user = self.context["request"].user
        ownership = obj.shopping_list_ownership.get(user=user)
        return CurrentUserShoppingListOwnershipSerializer(ownership).data


############################
# SHOPPING LIST OWNERSHIPS #
############################


class ReadOnlyShoppingListOwnershipSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer()

    class Meta:
        model = ShoppingListOwnership
        fields = (
            "id",
            "user",
            "shopping_list",
            "permission",
        )
        read_only_fields = fields


class PartialUpdateShoppingListOwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListOwnership
        fields = ("permission",)


class CreateShoppingListOwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingListOwnership
        fields = (
            "id",
            "user",
            "shopping_list",
            "permission",
        )


##########################
# SHOPPING LIST PRODUCTS #
##########################


class BuyListOfProductsSerializer(serializers.ModelSerializer):
    products = UpdatePriceShoppingListProductSerializer(source="shopping_list_product", many=True)

    class Meta:
        model = ShoppingList
        fields = (
            "id",
            "products",
        )
        read_only_fields = ("id",)

    def update(self, instance, validated_data):
        user = self.context["request"].user
        validated_products = validated_data.pop("shopping_list_product", [])
        validated_products_ids = [validated_product["id"] for validated_product in validated_products]
        modified_products = []
        for product in instance.shopping_list_product.filter(id__in=validated_products_ids):
            product.taken_by = user
            product.price = next(item["price"] for item in validated_products if item["id"] == product.id)
            product.status = ShoppingListProductStatus.BUYER
            modified_products.append(product)

        ShoppingListProduct.objects.bulk_update(modified_products, ["taken_by", "price", "status"])
        instance.update_is_archived()
        return instance


class ReadOnlyYourProductsSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingList
        fields = (
            "id",
            "products",
        )
        read_only_fields = fields

    @extend_schema_field(BasicListShoppingListProductSerializer(many=True))
    def get_products(self, obj):
        user = self.context["request"].user
        shopping_list_products = obj.shopping_list_product.filter(
            Q(status=ShoppingListProductStatus.TAKER) | Q(status=ShoppingListProductStatus.TAKER_MARKED),
            taken_by=user,
        )
        return BasicListShoppingListProductSerializer(shopping_list_products, many=True).data


class ShoppingListSummaryUsers(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "avatar",
            "products",
            "total_price",
        )
        read_only_fields = fields

    @extend_schema_field(BasicListShoppingListProductSerializer(many=True))
    def get_products(self, obj):
        shopping_list = self.context["shopping_list"]
        products = obj.shopping_list_product.filter(shopping_list=shopping_list).exclude(
            status=ShoppingListProductStatus.FREE
        )
        return BasicListShoppingListProductSerializer(products, many=True).data

    def get_total_price(self, obj) -> Decimal:
        shopping_list = self.context["shopping_list"]
        products = obj.shopping_list_product.filter(shopping_list=shopping_list, status=ShoppingListProductStatus.BUYER)
        return sum([product.price for product in products if product.price])


class ReadOnlySummaryProducts(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingList
        fields = (
            "id",
            "users",
        )
        read_only_fields = fields

    @extend_schema_field(ShoppingListSummaryUsers(many=True))
    def get_users(self, obj):
        users = User.objects.filter(id__in=obj.shopping_list_product.values_list("taken_by", flat=True))
        return ShoppingListSummaryUsers(users, many=True, context={"shopping_list": obj}).data
