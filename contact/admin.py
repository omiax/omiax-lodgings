from django.contrib import admin


from contact import models


class SingleInstanceAdminMixin(object):
    """Hides the "Add" button when there is already an instance."""

    # Preventing the creation of more than one "AboutUs" instance
    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        return super(SingleInstanceAdminMixin, self).has_add_permission(request)


class PhoneNumberAdmin(admin.StackedInline):
    model = models.PhoneNumber
    extra = 1


class EmailAddressAdmin(admin.StackedInline):
    model = models.EmailAddress
    extra = 1


class ContactAdmin(admin.ModelAdmin):
    inlines = [
        PhoneNumberAdmin,
        EmailAddressAdmin
    ]
    list_display = ['location', 'address']


class AboutUsAdmin(SingleInstanceAdminMixin, admin.ModelAdmin):
    pass


admin.site.register(models.AboutUs, AboutUsAdmin)
admin.site.register(models.Contact, ContactAdmin)
