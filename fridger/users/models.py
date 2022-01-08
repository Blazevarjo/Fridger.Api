from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Case, F, Q, Sum, When
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.translation import gettext as _

from fridger.utils.enums import (
    FridgeProductStatus,
    QuantityType,
    ShoppingListProductStatus,
)
from fridger.utils.models import BaseModel

from .managers import CustomUserManager, FriendQuerySet


def avatar_path(instance, filename):
    return f"avatar-{instance.id}"


class User(AbstractUser, BaseModel):
    email = models.EmailField(_("Email"), unique=True)
    username = models.CharField(_("Username"), max_length=40, unique=True)
    avatar = models.ImageField(_("Avatar"), blank=True, upload_to=avatar_path)
    can_use_real_name = models.BooleanField(_("Can display real name"), default=False)
    mobile_token = models.CharField(_("Mobile push token"), max_length=60, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    @property
    def friends(self):
        friends = Friend.objects.user_friends(self)
        return friends

    def food_stats(self, start_date=None, end_date=None):
        products = self.fridge_product_history
        if start_date:
            products = products.filter(created_at__gte=start_date)
        if end_date:
            products = products.filter(created_at__lte=end_date)

        stats = products.aggregate(
            eaten_liters=Coalesce(
                Sum(
                    Case(
                        When(
                            status=FridgeProductStatus.USED,
                            product__quantity_type=QuantityType.ML,
                            then=F("quantity") / 1000,
                        ),
                        When(
                            status=FridgeProductStatus.USED,
                            product__quantity_type=QuantityType.L,
                            then=F("quantity"),
                        ),
                        output_field=models.DecimalField(),
                    ),
                ),
                Decimal(0),
            ),
            eaten_kilograms=Coalesce(
                Sum(
                    Case(
                        When(
                            status=FridgeProductStatus.USED,
                            product__quantity_type=QuantityType.G,
                            then=F("quantity") / 1000,
                        ),
                        When(
                            status=FridgeProductStatus.USED,
                            product__quantity_type=QuantityType.KG,
                            then=F("quantity"),
                        ),
                        output_field=models.DecimalField(),
                    )
                ),
                Decimal(0),
            ),
            eaten_pieces=Coalesce(
                Sum("quantity", filter=Q(status=FridgeProductStatus.USED, product__quantity_type=QuantityType.PIECE)),
                Decimal(0),
            ),
            wasted_liters=Coalesce(
                Sum(
                    Case(
                        When(
                            status=FridgeProductStatus.WASTED,
                            product__quantity_type=QuantityType.ML,
                            then=F("quantity") / 1000,
                        ),
                        When(
                            status=FridgeProductStatus.WASTED,
                            product__quantity_type=QuantityType.L,
                            then=F("quantity"),
                        ),
                        output_field=models.DecimalField(),
                    )
                ),
                Decimal(0),
            ),
            wasted_kilograms=Coalesce(
                Sum(
                    Case(
                        When(
                            status=FridgeProductStatus.WASTED,
                            product__quantity_type=QuantityType.G,
                            then=F("quantity") / 1000,
                        ),
                        When(
                            status=FridgeProductStatus.WASTED,
                            product__quantity_type=QuantityType.KG,
                            then=F("quantity"),
                        ),
                        output_field=models.DecimalField(),
                    )
                ),
                Decimal(0),
            ),
            wasted_pieces=Coalesce(
                Sum("quantity", filter=Q(status=FridgeProductStatus.WASTED, product__quantity_type=QuantityType.PIECE)),
                Decimal(0),
            ),
        )
        return stats

    def money_spent_stats(self, start_date, end_date=timezone.datetime.now()):
        products = self.shopping_list_product
        if start_date and end_date:
            products = products.filter(updated_at__gte=start_date, updated_at__lte=end_date)
        stats = products.filter(status=ShoppingListProductStatus.BUYER).aggregate(money_spent=Sum("price"))
        return stats

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
