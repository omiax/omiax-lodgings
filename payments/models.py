from django.db import models
from django.conf import settings

import uuid
import datetime


# from environ import Env

from lodge.models import Lodge, Room

# env = Env()

# def current_year():
#     return datetime.date.today().year


def image_file_path(instance, filename):
    """Generate file path for lodge image"""
    return '/'.join(['payments', str(instance.lodge.name).replace(' ', '_'), filename])


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
    amount = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
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
    # Payment verification Image
    payment_image = models.ImageField(blank=True, null=True, upload_to=image_file_path)

    def __str__(self):
        return f"{self.amount} naira - {self.rent_start_date} to {self.rent_end_date}"  # noqa

    def save(self, *args, **kwargs):
        if self.lodge is None:
            self.lodge = self.room.lodge

        if self.transaction_id == "":
            self.transaction_id = uuid.uuid1()
            self.terms_agreed = True

        if self.rent_start_date is None:
            self.rent_start_date = datetime.date.today()
        if self.rent_end_date is None:
            self.rent_end_date = datetime.date.today() + datetime.timedelta(weeks=52)

        if not self.tenant_name:
            if self.tenant.first_name or self.tenant.last_name:
                self.tenant_name = f"{self.tenant.first_name} {self.tenant.last_name}"
            else:
                self.tenant_name = self.tenant.username

        super().save(*args, **kwargs)
