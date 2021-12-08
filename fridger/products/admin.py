from django.contrib import admin

from .models import FridgeProduct, FridgeProductHistory

admin.site.register(FridgeProduct)
admin.site.register(FridgeProductHistory)
