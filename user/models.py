from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.conf import settings

from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


# ^(\+\d{1,3}[- ]?)?\d{10}$
# ^(\+\d{1,3}[- ]?|[0])?\d{10}$
# ^(\+\d{1,3}[- ]?|[0])?\d{10}$
class User(AbstractUser):
    """Custom user model that adds extra fields"""

    phone_number = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(r"^(\+\d{1,3}[- ]?|[0])?\d{10}$")])
    country_code = models.CharField(
        default="+234",
        max_length=4,
        validators=[RegexValidator(r"^\+\d{1,3}[- ]?\d{1,5}$")])
    address = models.CharField(max_length=300)
    state = models.CharField(max_length=80)
    # personal details
    state_of_origin = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    place_of_work = models.CharField(max_length=255, blank=True, null=True)
    # Bank details for refund of caution fees
    bank_account_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=10, blank=True, null=True)

    # # @TODO force emails to be unique
    class Meta:
        unique_together = ('email', )


class EmergencyInfo(models.Model):
    tenant = models.OneToOneField(settings.AUTH_USER_MODEL,
                                  models.CASCADE,
                                  related_name="emergency")
    name = models.CharField(max_length=255, blank=False, null=True)
    contact_address = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    place_of_work = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(
        max_length=14,
        validators=[RegexValidator(r"^(\+\d{1,3}[- ]?|[0])?\d{10}$")])

    def __str__(self):
        return f'{self.name} - {self.contact_address} - {self.phone}'


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args,
                                 **kwargs):
    # @TODO: Update at production
    # the right form -> http://localhost:3000/confirmpassword/?tk=tokenhere
    # the current form -> /api/password_reset/?token=0514ef7a4ddaafc90b3ef63da4c4e33fe2d    # noqa

    email_plaintext_message = "http://139.162.231.92/confirmpassword/?tk={}".format(
        reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Omiax Accommodations"),
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email])
