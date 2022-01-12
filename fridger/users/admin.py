from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from fridger.users.models import Friend

User = get_user_model()


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "username")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    list_display = ("email", "date_joined", "is_staff")
    add_form = UserCreationForm

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "mobile_token",
                    "avatar",
                    "is_active",
                )
            },
        ),
    )
    ordering = ("date_joined",)
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                )
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Friend)
admin.site.unregister(Group)
