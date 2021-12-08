from django.db import models


class FridgeQuerySet(models.QuerySet):
    def user_fridges(self, user):
        return self.filter(fridge_ownership__user=user)
