import django_filters
from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Friend


class FriendFilter(filters.FilterSet):
    not_in_fridge = django_filters.UUIDFilter(method="filter_friends_not_in_fridge")
    not_in_shopping_list = django_filters.UUIDFilter(method="filter_friends_not_in_shopping_list")

    class Meta:
        model = Friend
        fields = ("is_accepted",)

    def filter_friends_not_in_fridge(self, queryset, name, value):
        return queryset.exclude(
            Q(friend_1__fridge_ownership__fridge=value) & Q(friend_2__fridge_ownership__fridge=value)
        )

    def filter_friends_not_in_shopping_list(self, queryset, name, value):
        return queryset.exclude(
            Q(friend_1__shopping_list_ownership__shopping_list=value)
            & Q(friend_2__shopping_list_ownership__shopping_list=value)
        )
