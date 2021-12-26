from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext as _
from djoser.views import UserViewSet as DjoserUserViewSet
from drf_spectacular.utils import extend_schema
from exponent_server_sdk import PushClient, PushMessage
from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import FriendFilter
from .models import Friend, User
from .permissions import IsFriendRequestReceiver, IsOneOfFriend
from .serializers import FriendSerializer, GeneralStatisticsSerializer, UserSerializer


def activate_account(request, uid, token):
    return render(request, "activate_account.html", {"uid": uid, "token": token})


def password_reset(request, uid, token):
    return render(request, "password_reset.html", {"uid": uid, "token": token})


class UpdateUserViewSet(DjoserUserViewSet):
    def perform_update(self, serializer):
        return super(viewsets.ModelViewSet, self).perform_update(serializer)


class UserDetailViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def retrieve(self, request, *args, **kwargs):
        """Get user by username."""
        return super().retrieve(request, *args, **kwargs)


class FriendViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = FriendSerializer
    filterset_class = FriendFilter
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
        friendship = serializer.save(friend_1=self.request.user)
        sender = friendship.friend_1
        receiver = friendship.friend_2
        if mobile_token := receiver.mobile_token:
            try:
                PushClient().publish(
                    PushMessage(
                        to=mobile_token,
                        title=_("You have received an invitation to become a friend"),
                        body=_("You have received an invitation to become a friend from %(username)s")
                        % {"username": sender.username},
                        data={"friend_id": str(friendship.id), "user_id": str(sender.id)},
                    )
                )
            except:
                pass

    def list(self, request, *args, **kwargs):
        """Friends of the currently logged in user."""
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Send friend request to user with given username."""
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Remove friend or deny friend request."""
        return super().destroy(request, *args, **kwargs)

    @extend_schema(request=None)
    @action(detail=True, methods=["post"], permission_classes=[IsFriendRequestReceiver])
    def accept(self, request, pk=None):
        """Accept friend request."""
        friend = self.get_object()
        friend.accept()
        serializer = self.get_serializer(friend)
        return Response(serializer.data)


class StatisticsView(generics.GenericAPIView):
    queryset = User.objects.none()
    serializer_class = GeneralStatisticsSerializer

    def get(self, request, format=None):
        user = request.user
        last_7_days_start_date = timezone.datetime.today() - timezone.timedelta(days=7)
        last_30_days_start_date = timezone.datetime.today() - timezone.timedelta(days=30)
        data = {
            "last_7_days": {
                "period_name": "last 7 days",
                "food_stats": user.food_stats(last_7_days_start_date),
                **user.money_spent_stats(last_7_days_start_date),
            },
            "last_30_days": {
                "food_stats": user.food_stats(last_30_days_start_date),
                **user.money_spent_stats(last_30_days_start_date),
            },
        }
        serializer = self.get_serializer(data)
        return Response(serializer.data)
