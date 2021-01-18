from rest_framework import permissions, generics

from notification import serializers, models


class NotificationListCreateView(generics.ListCreateAPIView):
    '''List and generate notifications'''
    # Notify
    serializer_class = serializers.NotificationSerializer
    # queryset = models.Notification.objects.all()

    # ensure only staff's can list all Notifications
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return models.Notification.objects.all()
        else:
            return models.Notification.objects.filter(receiver=user)


# class StaffNotificationListCreateView(generics.ListCreateAPIView):
#     permission_classes = (permissions.IsAdminUser,)

#     queryset = models.StaffNotificationList.objects.all()
#     serializer_class = serializers.StaffNotificationListSerializer
