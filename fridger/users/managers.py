from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.db.models import Q


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError("The Email must be set")
        email = email.strip().lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class FriendQuerySet(models.QuerySet):
    def user_friends(self, user):
        return self.filter(Q(friend_1=user) | Q(friend_2=user))

    def are_friends(self, user_1, user_2):
        return self.filter(
            Q(Q(friend_1=user_1) & Q(friend_2=user_2)) | Q(Q(friend_1=user_2) & Q(friend_2=user_1))
        ).exists()
