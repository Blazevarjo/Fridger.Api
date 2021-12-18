from django.contrib import admin

from .models import ShoppingList, ShoppingListFragment, ShoppingListOwnership

admin.site.register(ShoppingList)
admin.site.register(ShoppingListFragment)
admin.site.register(ShoppingListOwnership)
