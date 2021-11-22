from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fridger.users.permissions import IsFriendRequestReceiver
from fridger.users.serializers import FriendSerializer


def activate_account(request, uid, token):
    return render(request, "activate_account.html", {"uid": uid, "token": token})


def password_reset(request, uid, token):
    return render(request, "password_reset.html", {"uid": uid, "token": token})


class FriendViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FriendSerializer

    def get_queryset(self):
        user = self.request.user
        return user.friends

    def perform_create(self, serializer):
        serializer.save(friend_1=self.request.user)

    @extend_schema(request=None)
    @action(detail=True, methods=["post"], permission_classes=[IsFriendRequestReceiver])
    def accept(self, request, pk=None):
        friend = self.get_object()
        friend.accept()
        serializer = self.get_serializer(friend)
        return Response(serializer.data)
