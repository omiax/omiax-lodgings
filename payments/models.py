from django.db import models
from django.conf import settings

# from django.dispatch import receiver
# from django.db.models.signals import pre_save

# import datetime
# import requests
# from environ import Env

from lodge.models import Lodge, Room

# env = Env()

# def current_year():
#     return datetime.date.today().year


class Payment(models.Model):
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL,
                               models.SET_NULL,
                               blank=True,
                               null=True,
                               limit_choices_to={'is_staff': False})
    # room info
    lodge = models.ForeignKey(Lodge, models.SET_NULL, blank=True, null=True)
    room = models.ForeignKey(Room, models.SET_NULL, blank=True, null=True)

    tenant_name = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(default=0.00, max_digits=8, decimal_places=2)
    rent_start_date = models.DateField(blank=True, null=True)
    rent_end_date = models.DateField(blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, unique=True)
    terms_agreed = models.BooleanField(default=False)
    verified = models.CharField(max_length=20, default="unverified")

    # from the payment server //
    currency = models.CharField(blank=True, null=True, max_length=5)
    ip_address = models.CharField(blank=True, null=True, max_length=100)
    status = models.CharField(blank=True, null=True, max_length=100)
    created_at = models.DateTimeField(blank=True, null=True)
    amount_settled = models.DecimalField(default=0.00,
                                         max_digits=8,
                                         decimal_places=2)
    payment_ref = models.CharField(blank=True, null=True, max_length=255)
    payment_type = models.CharField(blank=True, null=True, max_length=100)
    payment_plan = models.CharField(blank=True, null=True, max_length=50)
    customer_id = models.CharField(blank=True, null=True, max_length=100)
    account_id = models.CharField(blank=True, null=True, max_length=100)
    app_fee = models.IntegerField(null=True, blank=True)
    merchant_fee = models.IntegerField(null=True, blank=True)

    manual_pay = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.amount} naira - {self.rent_start_date} to {self.rent_end_date}"  # noqa

    # def save(self, *args, **kwargs):

    #     if not self.id:
    #         self.name = f"{self.user.first_name} {self.user.last_name}"
    #     super().save(*args, **kwargs)
