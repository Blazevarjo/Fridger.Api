from rest_framework import serializers

from fridger.shopping_lists.models import ShoppingList, ShoppingListOwnership
from fridger.utils.enums import UserPermission


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = [
            "id",
            "name",
            "free_products_count",
            "taken_products_count",
            "bought_products_count",
        ]
        read_only_fields = (
            "id",
            "name",
        )

    def create(self, validated_data):
        user = self.context.get("request").user
        shopping_list = ShoppingList.objects.create(user, **validated_data)
        ShoppingListOwnership.objects.create(user=user, shopping_list=shopping_list, permission=UserPermission.ADMIN)
        return shopping_list


class ShoppingListDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "name",
            "free_products_count",
            "taken_products_count",
            "bought_products_count",
            "products",
        )
        read_only_fields = fields
