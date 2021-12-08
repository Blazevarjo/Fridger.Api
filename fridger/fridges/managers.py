from django.db import models


class FridgeQuerySet(models.QuerySet):
    def user_fridges(self, user):
        return self.filter(fridge_ownership__user=user)


class FridgeOwnershipsQuerySet(models.QuerySet):
    def user_fridge_ownerships(self, user):
        fridges_id = user.fridge_ownership.values_list("fridge__id", flat=True)
        return self.filter(fridge__in=fridges_id)
