from rest_framework import serializers

from notification.models import Notification, StaffNotificationList


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        # fields = "__all__"
        exclude = ['created_at', 'sender', 'receiver']


# class StaffNotificationListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StaffNotificationList
#         fields = "__all__"
