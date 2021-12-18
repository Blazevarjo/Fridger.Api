from django.db import models
from django.utils.translation import gettext as _


class UserPermission(models.TextChoices):
    CREATOR = "CREATOR", _("Creator")
    ADMIN = "ADMIN", _("Admin")
    WRITE = "WRITE", _("Write")
    READ = "READ", _("Read")


class QuantityType(models.TextChoices):
    PIECE = "PIECE", _("Piece")
    ML = "ML", _("Ml")
    L = "L", _("L")
    G = "G", _("G")
    KG = "KG", _("Kg")


class FridgeProductStatus(models.TextChoices):
    UNUSED = "UNUSED", _("Unused")
    USED = "USED", _("Used")
    WASTED = "WASTED", _("Wasted")
    UNTRACKED = "UNTRACKED", _("Untracked")


class ShoppingListProductStatus(models.TextChoices):
    FREE = "FREE", _("Free")
    TAKER = "TAKER", _("Taker")
    TAKER_MARKED = "TAKER_MARKED", _("Taker marked")
    BUYER = "BUYER", _("Buyer")
