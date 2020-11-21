from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from user import models

# class CustomUserAdmin(admin.ModelAdmin):
#     model = models.User

# admin.site.register(models.User, CustomUserAdmin)


class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["username", "phone_number", "email"]
    fieldsets = (
        (None, {
            "fields": ("username", "password")
        }),
        (
            _("Personal Info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "country_code",
                    "phone_number",
                    "email",
                    "address",
                    "state",
                )
            },
        ),
        (_("Permissions"), {
            "fields": ("is_active", "is_staff", "is_superuser", "groups")
        }),
        (_("Important dates"), {
            "fields": ("last_login", "date_joined")
        }),
    )
    add_fieldsets = ((
        None,
        {
            "classes": ("wide", ),
            "fields": (
                "username",
                "password1",
                "password2",
                "country_code",
                "phone_number",
            ),
        },
    ), )


admin.site.register(models.User, UserAdmin)
