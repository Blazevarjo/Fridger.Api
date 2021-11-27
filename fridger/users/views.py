from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fridger.users.models import Friend
from fridger.users.permissions import IsFriendRequestReceiver, IsOneOfFriend
from fridger.users.serializers import FriendSerializer


def activate_account(request, uid, token):
    return render(request, "activate_account.html", {"uid": uid, "token": token})


def password_reset(request, uid, token):
    return render(request, "password_reset.html", {"uid": uid, "token": token})


class FriendViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = FriendSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_accepted"]
    queryset = Friend.objects.none()

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action == "destroy":
            permission_classes = [IsOneOfFriend]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        return user.friends

    def perform_create(self, serializer):
        serializer.save(friend_1=self.request.user)

    def list(self, request, *args, **kwargs):
        """
        Friends of the currently logged in user
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Send friend request to user with given username
        """
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Remove friend or deny friend request
        """
        return super().destroy(request, *args, **kwargs)

    @extend_schema(request=None)
    @action(detail=True, methods=["post"], permission_classes=[IsFriendRequestReceiver])
    def accept(self, request, pk=None):
        """
        Accept friend request
        """
        friend = self.get_object()
        friend.accept()
        serializer = self.get_serializer(friend)
        return Response(serializer.data)
