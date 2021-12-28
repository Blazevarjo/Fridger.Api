from django.utils.translation import gettext as _
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Friend, User

#########
# USERS #
#########


class BasicDisplayUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "avatar",
        )
        read_only_fields = fields


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "avatar",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "avatar",
            "mobile_token",
        )
        read_only_fields = ("email",)
        extra_kwargs = {"mobile_token": {"write_only": True}}

    def validate_mobile_token(self, value: str):
        if value.startswith("ExponentPushToken[") and value.endswith("]"):
            return value
        raise serializers.ValidationError(_('Token should be in form: "ExponentPushToken[token]"'))


###########
# FRIENDS #
###########


class CreateFriendSerializer(serializers.Serializer):
    friend = serializers.CharField()


class FriendSerializer(serializers.ModelSerializer):
    friend = serializers.SerializerMethodField()
    is_my_request = serializers.SerializerMethodField()
    friend_to_add = serializers.UUIDField(write_only=True)

    class Meta:
        model = Friend
        fields = (
            "id",
            "friend",
            "created_at",
            "is_accepted",
            "friend_to_add",
            "is_my_request",
        )
        read_only_fields = (
            "friend",
            "is_my_request",
            "created_at",
            "is_accepted",
        )

    @extend_schema_field(BasicUserSerializer)
    def get_friend(self, obj):
        user = self.context.get("request").user
        friend = obj.get_friend(user)
        return BasicUserSerializer(friend).data

    def get_is_my_request(self, obj) -> bool:
        user = self.context.get("request").user
        return obj.is_friend_creator(user)

    def validate(self, attrs):
        friend_1 = self.context.get("request").user
        friend_2_id = attrs.pop("friend_to_add")

        try:
            friend_2 = User.objects.get(id=friend_2_id)
            attrs["friend_2"] = friend_2
        except User.DoesNotExist:
            raise serializers.ValidationError({"friend_to_add": f"User '{friend_2_id}' does not exist."})

        if Friend.objects.are_friends(friend_1, friend_2):
            raise serializers.ValidationError(f"You are already friends with user '{friend_2_id}'")

        return attrs


##############
# STATISTICS #
##############


class FoodDecimalsSerializer(serializers.Serializer):
    liters = serializers.DecimalField(max_digits=10, decimal_places=3, read_only=True)
    kilograms = serializers.DecimalField(max_digits=10, decimal_places=3, read_only=True)
    pieces = serializers.DecimalField(max_digits=10, decimal_places=3, read_only=True)


class FoodStatisticsSerializer(serializers.Serializer):
    eaten = serializers.SerializerMethodField()
    wasted = serializers.SerializerMethodField()

    @extend_schema_field(FoodDecimalsSerializer)
    def get_eaten(self, obj):
        return FoodDecimalsSerializer(
            {
                "liters": obj["eaten_liters"],
                "kilograms": obj["eaten_kilograms"],
                "pieces": obj["eaten_pieces"],
            }
        ).data

    @extend_schema_field(FoodDecimalsSerializer)
    def get_wasted(self, obj):
        return FoodDecimalsSerializer(
            {
                "liters": obj["wasted_liters"],
                "kilograms": obj["wasted_kilograms"],
                "pieces": obj["wasted_pieces"],
            }
        ).data


class StatisticsSerializer(serializers.Serializer):
    food_stats = FoodStatisticsSerializer(read_only=True)
    money_spent = serializers.DecimalField(max_digits=9, decimal_places=2, read_only=True)


class GeneralStatisticsSerializer(serializers.Serializer):
    last_7_days = StatisticsSerializer(read_only=True)
    last_30_days = StatisticsSerializer(read_only=True)
