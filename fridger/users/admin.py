from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from fridger.users.models import Friend

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_display = ("email", "date_joined", "is_staff")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "username", "can_use_real_name", "avatar", "is_active")},
        ),
    )
    ordering = ("date_joined",)
    add_fieldsets = ((None, {"fields": ("email", "password")}),)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Friend)
admin.site.unregister(Group)
