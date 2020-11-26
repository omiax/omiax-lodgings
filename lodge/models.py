from django.db import models
from django.conf import settings

# https://stackoverflow.com/questions/3648421/only-accept-a-certain-file-type-in-filefield-server-side
# from django.core.validators import FileExtensionValidator

# import datetime

# def current_year():
#     return datetime.date.today().year


def image_file_path(instance, filename):
    """Generate file path for lodge image"""
    return '/'.join(['lodges', str(instance.name), filename])


# def agreement_file_path(instance, filename):
#     """Generate file path for lodge image"""
#     return '/'.join(['lodges', 'agreement', str(instance.name), filename])


class Lodge(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=80)
    country = models.CharField(max_length=100, default="Nigeria")
    image = models.ImageField(blank=True, null=True, upload_to=image_file_path)
    water = models.BooleanField(blank=True, null=True)
    electricity = models.BooleanField(blank=True, null=True)
    num_of_rooms = models.PositiveSmallIntegerField(null=False)
    details = models.CharField(max_length=100, blank=True, null=True)
    owner = models.CharField(default="omiax",
                             max_length=100,
                             blank=True,
                             null=True)
    standard_price = models.DecimalField(default=0.00,
                                         max_digits=8,
                                         decimal_places=2)

    # agreement = models.FileField(
    #     blank=True,
    #     null=True,
    #     upload_to=agreement_file_path,
    #     validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    # def save(self, *args, **kwargs):

    def __str__(self):
        return self.name

# @TODO add unigue=True for tenant to room to make like a OneToOne


class Room(models.Model):
    lodge = models.ForeignKey(Lodge, models.CASCADE, related_name="rooms")
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL,
                               models.SET_NULL,
                               blank=True,
                               null=True,
                               limit_choices_to={'is_staff': False},
                               related_name="tenants")
    room_number = models.PositiveSmallIntegerField(null=False)
    floor = models.IntegerField(default=0)
    occupied = models.BooleanField(default=False)
    room_price = models.DecimalField(default=0.00,
                                     max_digits=8,
                                     decimal_places=2)
    room_mates = models.CharField(max_length=255, blank=True, null=True)
    rent_start_date = models.DateField(blank=True, null=True)
    rent_end_date = models.DateField(blank=True, null=True)
    transaction_id = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        unique_together = (
            'lodge',
            'room_number',
        )
        ordering = (
            'lodge',
            'room_number',
        )

    def save(self, *args, **kwargs):
        if self.tenant is not None:
            self.occupied = True
        else:
            self.occupied = False

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.lodge} - Room: {self.room_number}'


# class Legal(models.Model):
#     lodge = models.ForeignKey(Lodge, models.CASCADE, related_name="lodge")
#     agreement = models.CharField(blank=True, null=True)
#     terms_agreed = models.BooleanField(blank=True, null=True)
