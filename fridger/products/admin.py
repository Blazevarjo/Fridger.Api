from django.contrib import admin

from .models import FridgeProduct, FridgeProductHistory, ShoppingListProduct

admin.site.register(FridgeProduct)
admin.site.register(FridgeProductHistory)
admin.site.register(ShoppingListProduct)
