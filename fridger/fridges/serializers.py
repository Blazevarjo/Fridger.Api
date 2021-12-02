from rest_framework import serializers

from fridger.fridges.models import Fridge


class CreateOrUpdateFridgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fridge
        fields = ["id", "name"]

    def create(self, validated_data):
        user = self.context.get("request").user
        return Fridge.objects.create_with_permission(user, **validated_data)
