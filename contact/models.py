from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from tinymce.models import HTMLField


class SingleInstanceMixin(object):
    """Makes sure that no more than one instance of a given model is created."""

    # Preventing the creation of more than one "AboutUs" instance
    def clean(self):
        model = self.__class__
        if (model.objects.count() > 0 and self.id != model.objects.get().id):
            raise ValidationError("Can only create 1 %s instance" % model.__name__)
        super(SingleInstanceMixin, self).clean()


class Contact(models.Model):
    location = models.CharField(max_length=255)
    address = models.TextField(max_length=255)

    def __str__(self):
        return self.location


class PhoneNumber(models.Model):
    # inline for contacts
    contact_phone = models.ForeignKey(Contact, models.CASCADE,
                                      related_name="contact_phone")
    phone = models.CharField(max_length=14, null=True, blank=True,
                             validators=[RegexValidator(r"^(\+\d{1,3}[- ]?|[0])?\d{10}$")])

    def __str__(self):
        return self.phone


class EmailAddress(models.Model):
    # inline for contacts
    contact_email = models.ForeignKey(Contact, models.CASCADE, related_name="contact_email")
    email = models.EmailField()

    def __str__(self):
        return self.email


class AboutUs(SingleInstanceMixin, models.Model):
    about_us = HTMLField(blank=True, null=True)

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"

    def __str__(self):
        return "About Us"
