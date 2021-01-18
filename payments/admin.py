from django.contrib import admin
from django.utils.translation import gettext as _

from payments import models


class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "tenant",
        "tenant_name",
        "amount",
        "rent_start_date",
        "rent_end_date",
        "transaction_id",
        "lodge_name",
        "verified",
    ]
    # list_editable = ('verified',)
    list_filter = ("lodge", "manual_pay")
    fieldsets = ((_("Payment Details"), {
        "fields":
        ("tenant", "lodge", "room", "tenant_name", "amount", "rent_start_date",
         "rent_end_date", "transaction_id", "terms_agreed", "verified", "lodge_name", "manual_pay",
         "payment_image")
    }), (_("Transaction Information"), {
        "fields":
        ("currency", "ip_address", "status", "created_at", "amount_settled",
         "payment_ref", "payment_type", "payment_plan", "customer_id",
         "account_id", "app_fee", "merchant_fee", )
    }))
    readonly_fields = ("lodge", "transaction_id", "currency", "ip_address", "status", "created_at", "amount_settled",
                       "payment_ref", "payment_plan", "customer_id", "account_id", "app_fee", "merchant_fee",
                       )
    actions = ["verified_payment"]

    def verified_payment(self, request, queryset):
        for obj in queryset:
            obj.verified = "verified"
            obj.save()
    verified_payment.short_description = "Verify selected payments"


admin.site.register(models.Payment, PaymentAdmin)
