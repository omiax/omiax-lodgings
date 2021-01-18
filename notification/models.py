from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


class Notification(models.Model):
    TYPE = (
        ('N', 'Normal'),
        ('D', 'Danger'),
    )
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL,
                               null=True, blank=True, related_name="message_sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 models.CASCADE, related_name="message_receiver")
    topic = models.CharField(max_length=50, null=True, blank=True)
    message = models.TextField(max_length=255)
    rating = models.CharField(max_length=1, choices=TYPE, default="N")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.receiver} - created: {self.created_at.strftime("%a, %d/%m/%Y")}'


class StaffNotificationList(models.Model):
    staff = models.ForeignKey(settings.AUTH_USER_MODEL,
                              models.CASCADE,
                              blank=True,
                              null=True,
                              limit_choices_to={'is_staff': True},
                              related_name="staff_member")
    name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True, unique=True,)
    phone_number = models.CharField(max_length=14, null=True, blank=True, unique=True,
                                    validators=[RegexValidator(r"^(\+\d{1,3}[- ]?|[0])?\d{10}$")])

    def __str__(self):
        return f'{self.staff} - {self.name} - {self.email} - {self.phone_number}'
