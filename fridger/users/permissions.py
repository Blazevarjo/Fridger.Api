from rest_framework import permissions


class IsFriendRequestReceiver(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.friend_2 == request.user
