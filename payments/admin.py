from django.contrib import admin
from payments import models
from django.utils.translation import gettext as _


class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "tenant",
        "tenant_name",
        "amount",
        "rent_start_date",
        "rent_end_date",
        "transaction_id",
        "verified",
    ]
    fieldsets = ((_("Payment Details"), {
        "fields":
        ("tenant", "lodge", "room", "tenant_name", "amount", "rent_start_date",
         "rent_end_date", "transaction_id", "terms_agreed", "verified")
    }), (_("Transaction Information"), {
        "fields":
        ("currency", "ip_address", "status", "created_at", "amount_settled",
         "payment_ref", "payment_type", "payment_plan", "customer_id",
         "account_id", "app_fee", "merchant_fee", "manual_pay")
    }))


admin.site.register(models.Payment, PaymentAdmin)
