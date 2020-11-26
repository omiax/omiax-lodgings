from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from user import models

# class CustomUserAdmin(admin.ModelAdmin):
#     model = models.User

# admin.site.register(models.User, CustomUserAdmin)


class EmergencyInfoInline(admin.StackedInline):
    model = models.EmergencyInfo


class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["username", "phone_number", "email", "get_lodge"]
    inlines = [
        EmergencyInfoInline,
    ]
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
                    # personal details
                    "state_of_origin",
                    "occupation",
                    "place_of_work",
                    # Bank details for caution fees refund
                    "bank_account_name",
                    "account_number",
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

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        return qs.prefetch_related('tenants')

    def get_lodge(self, obj):
        return list(obj.tenants.all())


class EmergencyInfoAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'name', 'contact_address', 'phone']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.EmergencyInfo)
