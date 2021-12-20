from django.contrib import admin

from .models import ShoppingList, ShoppingListOwnership

admin.site.register(ShoppingList)
admin.site.register(ShoppingListOwnership)
