from django.db import models


class ShoppingListQuerySet(models.QuerySet):
    def user_shopping_lists(self, user):
        return self.filter(shopping_list_ownership__user=user)


class ShoppingListOwnershipQuerySet(models.QuerySet):
    def user_shopping_list_ownerships(self, user):
        shopping_lists_ids = user.shopping_list_ownership.values_list("shopping_list__id", flat=True)
        return self.filter(shopping_list__in=shopping_lists_ids)
