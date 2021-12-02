from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from fridger.fridges.managers import FridgeQuerySet
from fridger.utils.enums import UserPermission
from fridger.utils.models import BaseModel

User = get_user_model()


class Fridge(BaseModel):
    name = models.CharField(_("Name"), max_length=60)

    objects = FridgeQuerySet.as_manager()

    @property
    def shared_with_count(self):
        # reduce by one because of the owner
        return self.fridge_ownership.count() - 1

    @property
    def products_count(self):
        return self.fridge_product.filter(is_available=True).count()

    def __str__(self) -> str:
        return self.name


class FridgeOwnership(BaseModel):
    user = models.ForeignKey(User, related_name="fridge_ownership", on_delete=models.CASCADE)
    fridge = models.ForeignKey(Fridge, related_name="fridge_ownership", on_delete=models.CASCADE)
    permission = models.IntegerField(
        _("User permission to fridger"), choices=UserPermission.choices, default=UserPermission.READ
    )

    def __str__(self) -> str:
        return f"{self.fridge.name} - {self.user.email}"
