from django.contrib.auth.models import AbstractUser
from django.db import models

from fridger.utils.models import BaseModel

from .managers import CustomUserManager, FriendQuerySet


def avatar_path(instance, filename):
    return f"avatar-{instance.id}"


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True, blank=True, null=True)
    avatar = models.ImageField(blank=True, upload_to=avatar_path)
    can_use_real_name = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Friend(BaseModel):
    friend_1 = models.ForeignKey(User, related_name="friend_creator", on_delete=models.CASCADE)
    friend_2 = models.ForeignKey(User, related_name="friend", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    objects = FriendQuerySet.as_manager()
