from django.contrib import admin

from notification import models


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['receiver', 'rating', 'created_at']


class StaffNotificationListAdmin(admin.ModelAdmin):
    list_display = ['staff', 'name', 'email', 'phone_number']
    list_editable = ['email', 'phone_number']


admin.site.register(models.Notification, NotificationAdmin)
admin.site.register(models.StaffNotificationList, StaffNotificationListAdmin)
