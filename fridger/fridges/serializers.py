from django.utils.translation import gettext as _
from drf_spectacular.utils import extend_schema_field
from rest_framework import exceptions, serializers

from fridger.users.serializers import BasicUserSerializer
from fridger.utils.enums import UserPermission

from .models import Fridge, FridgeOwnership

###########
# FRIDGES #
###########


class BasicFridgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fridge
        fields = (
            "id",
            "name",
        )
        read_only_fields = fields


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

    def validate(self, attrs):
        request_user = self.context.get("request").user
        fridge = attrs.get("fridge")
        try:
            ownership = request_user.fridge_ownership.get(fridge=fridge)
        except FridgeOwnership.DoesNotExist:
            raise exceptions.PermissionDenied(_("User does not belong to this fridge."))

        if ownership.permission not in [UserPermission.CREATOR, UserPermission.ADMIN, UserPermission.WRITE]:
            raise exceptions.PermissionDenied(_("User does not have permission to add friend to this fridge."))

        return attrs
