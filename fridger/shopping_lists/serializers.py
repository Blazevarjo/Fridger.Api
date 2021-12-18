from django.contrib.auth import get_user_model
from django.db.models import Q
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from fridger.products.serializers import (
    BasicListShoppingListProductSerializer,
    ListShoppingListProductSerializer,
)
from fridger.users.serializers import BasicUserSerializer
from fridger.utils.enums import ShoppingListProductStatus, UserPermission

from .models import ShoppingList, ShoppingListFragment, ShoppingListOwnership

User = get_user_model()


class PartialUpdateShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ("name",)


class ShoppingListSerializer(serializers.ModelSerializer):
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
        )
        read_only_fields = (
            "id",
            "free_products_count",
            "taken_products_count",
            "bought_products_count",
            "is_archived",
            "is_shared",
        )

    def create(self, validated_data):
        user = self.context.get("request").user
        shopping_list = ShoppingList.objects.create(**validated_data)
        ShoppingListOwnership.objects.create(user=user, shopping_list=shopping_list, permission=UserPermission.CREATOR)
        return shopping_list


class ShoppingListDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "name",
            "is_archived",
            "is_shared",
            "free_products_count",
            "taken_products_count",
            "bought_products_count",
            "products",
        )
        read_only_fields = fields


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


class ShoppingListFragmentSerializer(serializers.ModelSerializer):
    products = BasicListShoppingListProductSerializer(many=True)

    class Meta:
        model = ShoppingListFragment
        fields = (
            "id",
            "price",
            "products",
        )
        read_only_fields = fields


class ReadOnlyYourProductsSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    # shopping_list_fragments = serializers.SerializerMethodField()

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
            created_by=user,
        )
        return BasicListShoppingListProductSerializer(shopping_list_products, many=True).data

    # @extend_schema_field(ShoppingListFragmentSerializer(many=True))
    # def get_shopping_list_fragments(self, obj):
    #     user = self.context["request"].user
    #     shopping_list_fragments = obj.shopping_list_fragment.get(user=user)
    #     return ShoppingListFragmentSerializer(shopping_list_fragments, many=True).data


class ReadOnlyAllProducts(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingList
        fields = (
            "id",
            "products",
        )
        read_only_fields = fields

    @extend_schema_field(ListShoppingListProductSerializer(many=True))
    def get_products(self, obj):
        user = self.context["request"].user
        shopping_list_products = obj.shopping_list_product.filter(created_by=user)
        return ListShoppingListProductSerializer(shopping_list_products, many=True).data


class ShoppingListSummaryUsers(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    fragments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "avatar",
            "products",
            "fragments",
        )

    @extend_schema_field(BasicListShoppingListProductSerializer(many=True))
    def get_products(self, obj):
        shopping_list = self.context["shopping_list"]
        shopping_list_products = obj.shopping_list_product.filter(shopping_list=shopping_list)
        return BasicListShoppingListProductSerializer(shopping_list_products, many=True).data

    @extend_schema_field(ShoppingListFragmentSerializer(many=True))
    def get_fragments(self, obj):
        shopping_list = self.context["shopping_list"]
        shopping_list_fragments = obj.shopping_list_fragment.filter(shopping_list=shopping_list)
        return ShoppingListFragmentSerializer(shopping_list_fragments, many=True).data


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
        users = obj.shopping_list_product.values_list("created_by", flat=True)
        return ShoppingListSummaryUsers(users, many=True, context={"shopping_list_id": obj.id})
