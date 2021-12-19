from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from fridger.users.serializers import BasicUserSerializer
from fridger.utils.enums import UserPermission

from .models import Fridge, FridgeOwnership

###########
# FRIDGES #
###########


class FridgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fridge
        fields = (
            "id",
            "name",
            "shared_with_count",
            "products_count",
        )
        read_only_fields = (
            "id",
            "shared_with_count",
            "products_count",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        fridge = Fridge.objects.create(**validated_data)
        FridgeOwnership.objects.create(user=user, fridge=fridge, permission=UserPermission.CREATOR)
        return fridge


class CurrentUserFridgeOwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeOwnership
        fields = (
            "id",
            "permission",
        )
        read_only_fields = fields


class FridgeDetailSerializer(serializers.ModelSerializer):
    my_ownership = serializers.SerializerMethodField()

    class Meta:
        model = Fridge
        fields = (
            "id",
            "name",
            "shared_with_count",
            "products_count",
            "my_ownership",
        )
        read_only_fields = fields

    @extend_schema_field(CurrentUserFridgeOwnershipSerializer)
    def get_my_ownership(self, obj):
        user = self.context["request"].user
        ownership = obj.fridge_ownership.get(user=user)
        return CurrentUserFridgeOwnershipSerializer(ownership).data


#####################
# FRIDGE OWNERSHIPS #
#####################


class ReadOnlyFridgeOwnershipSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer()

    class Meta:
        model = FridgeOwnership
        fields = (
            "id",
            "user",
            "fridge",
            "permission",
        )
        read_only_fields = fields


class PartialUpdateFridgeOwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeOwnership
        fields = ("permission",)


class CreateFridgeOwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeOwnership
        fields = (
            "id",
            "user",
            "fridge",
            "permission",
        )
