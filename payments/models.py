from django.db import models
from django.conf import settings

import datetime


def current_year():
    return datetime.date.today().year


class Payments(models.Model):
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECTED)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    year = models.PositiveIntegerField(default=current_year)

    def __str__(self):
        return f"{self.amount} naira - {self.year}"
