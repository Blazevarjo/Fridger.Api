from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q

from fridger.utils.models import BaseModel

from .managers import CustomUserManager


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(blank=True)
    can_use_real_name = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    @property
    def friends(self):
        return Friend.objects.filter(Q(friend_1=self.user) | Q(friend_2=self.user))

    def __str__(self):
        return self.email


class Friend(BaseModel):
    friend_1 = models.ForeignKey(User, related_name="friend_creator")
    friend_2 = models.ForeignKey(User, related_name="friend")
    created_at = models.DateTimeField(auto_now_add=True)
