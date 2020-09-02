from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


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
