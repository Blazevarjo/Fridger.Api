from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.translation import gettext as _

from fridger.fridges.managers import FridgeOwnershipsQuerySet, FridgeQuerySet
from fridger.utils.enums import UserPermission
from fridger.utils.models import BaseModel

User = get_user_model()


class Fridge(BaseModel):
    name = models.CharField(_("Name"), max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = FridgeQuerySet.as_manager()

    @property
    def shared_with_count(self) -> int:
        # reduce by one because of the owner
        return self.fridge_ownership.count() - 1

    @property
    def products_count(self) -> int:
        return self.fridge_product.filter(is_available=True).count()

    @property
    def products(self):
        return self.fridge_product.filter(is_available=True)

    def __str__(self) -> str:
        return self.name


class FridgeOwnership(BaseModel):
    user = models.ForeignKey(User, related_name="fridge_ownership", on_delete=models.CASCADE)
    fridge = models.ForeignKey(Fridge, related_name="fridge_ownership", on_delete=models.CASCADE)
    permission = models.CharField(
        _("User permission to fridger"), choices=UserPermission.choices, default=UserPermission.READ, max_length=7
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = FridgeOwnershipsQuerySet.as_manager()

    def __str__(self) -> str:
        return f"{self.fridge.name} - {self.user.email}"


@receiver(signals.post_delete, sender=FridgeOwnership)
def post_delete_signal(sender, instance, **kwargs):
    if not instance.fridge.fridge_ownership.filter(
        permission__in=[UserPermission.CREATOR, UserPermission.ADMIN]
    ).exists():
        try:
            new_admin = instance.fridge.fridge_ownership.earliest("created_at")
            new_admin.permission = UserPermission.ADMIN
            new_admin.save()
        except FridgeOwnership.DoesNotExist:
            pass
