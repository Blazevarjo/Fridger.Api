from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from fridger.utils.models import BaseModel

from .managers import CustomUserManager, FriendQuerySet


def avatar_path(instance, filename):
    return f"avatar-{instance.id}"


class User(AbstractUser, BaseModel):
    email = models.EmailField(_("Email"), unique=True)
    username = models.CharField(_("Username"), max_length=40, unique=True)
    avatar = models.ImageField(_("Avatar"), blank=True, upload_to=avatar_path)
    can_use_real_name = models.BooleanField(_("Can display real name"), default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    @property
    def friends(self):
        friends = Friend.objects.user_friends(self)
        return friends

    def __str__(self):
        return self.email


class Friend(BaseModel):
    friend_1 = models.ForeignKey(User, related_name="friend_creator", on_delete=models.CASCADE)
    friend_2 = models.ForeignKey(User, related_name="friend", on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    is_accepted = models.BooleanField(_("Is friend request accepted"), default=False)

    objects = FriendQuerySet.as_manager()

    def accept(self):
        self.is_accepted = True
        self.save()

    def is_in_friendship(self, current_user) -> bool:
        return current_user in [self.friend_1, self.friend_2]

    def get_friend(self, current_user) -> User:
        if current_user == self.friend_1:
            return self.friend_2
        return self.friend_1

    def is_friend_creator(self, current_user) -> bool:
        return self.friend_1 == current_user

    def __str__(self) -> str:
        return f"{self.friend_1} - {self.friend_2}"
