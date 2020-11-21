from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from django.dispatch import receiver
from django.urls import reverse
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


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args,
                                 **kwargs):
    # the right form -> http://localhost:3000/confirmpassword/?tk=tokenhere
    # the current form -> /api/password_reset/?token=0514ef7a4ddaafc90b3ef63da4c4e33fe2d    # noqa
    email_plaintext_message = "{}?token={}".format(
        reverse('password_reset:reset-password-request'),
        reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Omiax Lodgings"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email])
