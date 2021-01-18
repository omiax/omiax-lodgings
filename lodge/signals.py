from django.dispatch import receiver
from django.db.models.signals import post_save

from lodge.models import Lodge, Room
# from payments import Payments
# @TODO Caution


@receiver(post_save, sender=Lodge)
def generate_rooms(sender, instance, created, **kwargs):
    if created:
        room_flats = instance.num_of_flats
        objs = [
            Room(lodge=instance,
                 room_number=i,
                 room_price=instance.standard_price)
            for i in range(1, room_flats + 1)
        ]
        Room.objects.bulk_create(objs)

    if not created:
        updates = Room.objects.filter(lodge=instance).in_bulk()
        # print(updates)

        for x, y in updates.items():
            updates[x].room_price = instance.standard_price

        if hasattr(Room.objects, 'bulk_update') and updates:
            # Use the new method
            Room.objects.bulk_update(updates.values(), ['room_price'],
                                     batch_size=100)


# @receiver(post_save, sender=Room)
# def save_payment_transaction(sender, instance, created, **kwargs):
#     if not created:
#         if instance.occupied:
#             pay = Payments(tenant=instance.tenant,
#                            amount=instance.room_price,
#                            rent_start_date=instance.rent_start_date,
#                            rent_end_date=instance.rent_end_date)
#             pay.save()
