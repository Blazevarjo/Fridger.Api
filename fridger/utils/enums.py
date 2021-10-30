from django.db import models


class Ownership(models.IntegerChoices):
    ADMIN = 1
    WRITE = 2
    READ = 3


class QuantityType(models.IntegerChoices):
    PIECE = 1
    ML = 2
    L = 3
    G = 4
    KG = 5


class FridgeProductStatus(models.IntegerChoices):
    UNUSED = 1
    USED = 2
    WASTER = 3
    UNTRACKED = 4


class ShoppingListProductStatus(models.IntegerChoices):
    CREATOR = 1
    BUYER = 2
    TAKER = 3
