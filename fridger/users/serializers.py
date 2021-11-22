from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Friend, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "avatar", "can_use_real_name")
        read_only_fields = ("email",)


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "avatar", "can_use_real_name")


class CreateFriendSerializer(serializers.Serializer):
    friend = serializers.CharField()


class FriendSerializer(serializers.ModelSerializer):
    friend = serializers.SerializerMethodField()
    friend_to_add = serializers.CharField(write_only=True)

    class Meta:
        model = Friend
        fields = (
            "id",
            "friend",
            "created_at",
            "is_accepted",
            "friend_to_add",
        )
        read_only_fields = (
            "friend",
            "created_at",
            "is_accepted",
        )

    @extend_schema_field(BasicUserSerializer)
    def get_friend(self, obj):
        user = self.context.get("request").user
        friend = obj.get_friend(user)
        return BasicUserSerializer(friend).data

    def validate(self, attrs):
        friend_1 = self.context.get("request").user
        friend_2_username = attrs.pop("friend_to_add")

        try:
            friend_2 = User.objects.get(username=friend_2_username)
            attrs["friend_2"] = friend_2
        except User.DoesNotExist:
            raise serializers.ValidationError({"friend_to_add": f"User '{friend_2_username}' does not exist."})

        if Friend.objects.is_friend(friend_1, friend_2):
            raise serializers.ValidationError(f"You are already friends with user '{friend_2_username}'")

        return attrs
