from django.contrib import admin

from .models import Fridge, FridgeOwnership

# Register your models here.
admin.site.register(Fridge)
admin.site.register(FridgeOwnership)
