from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


def image_file_path(instance, filename):
    """Generate file path for lodge image"""
    return '/'.join(['lodges', str(instance.name), filename])


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

    def __str__(self):
        return self.name


# class Legal(models.Model):
#     lodge = models.ForeignKey(Lodge, models.CASCADE, related_name="lodge")
#     terms_n_conditions = models.CharField(blank=True, null=True)
#     agree = models.BooleanField(blank=True, null=True)


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


@receiver(post_save, sender=Lodge)
def generate_rooms(sender, instance, created, **kwargs):
    if created:
        room_nums = instance.num_of_rooms
        objs = [
            Room(lodge=instance,
                 room_number=i,
                 room_price=instance.standard_price)
            for i in range(1, room_nums + 1)
        ]
        Room.objects.bulk_create(objs)
