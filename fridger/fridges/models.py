from django.contrib.auth import get_user_model
from django.db import models

from fridger.utils.enums import Ownership
from fridger.utils.models import BaseModel

User = get_user_model()


class Fridge(BaseModel):
    name = models.CharField(max_length=60, blank=True)


class FridgeOwnership(BaseModel):
    user = models.ForeignKey(User, related_name="fridge_ownership", on_delete=models.RESTRICT)
    fridge = models.ForeignKey(Fridge, related_name="fridge_ownership", on_delete=models.CASCADE)
    ownership = models.IntegerField(choices=Ownership.choices, default=Ownership.READ)
