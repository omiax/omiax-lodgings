from django.dispatch import receiver
from django.db.models.signals import post_save

from django_q.tasks import async_task  # type: ignore

from notification.models import Notification, StaffNotificationList


# @receiver(post_save, sender=Notification, dispatch_uid="notify_tenant")
# def notify_tenant(sender, instance, created, **kwargs):
#     # Send the notification alert

@receiver(post_save, sender=StaffNotificationList, dispatch_uid="edit_staff")
def edit_staff(sender, instance, created, **kwargs):

    if instance.staff is not None:
        if instance.name is None:
            instance.name = f'{instance.staff.username}'
