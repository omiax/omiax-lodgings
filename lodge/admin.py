from django.contrib import admin
from lodge import models


class LodgeAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'address', 'state', 'num_of_rooms', 'details', 'owner'
    ]


class RoomAdmin(admin.ModelAdmin):
    list_display = [
        'lodge', 'room_number', 'tenant', 'occupied', 'rent_start_date',
        'rent_end_date'
    ]


admin.site.register(models.Lodge, LodgeAdmin)
admin.site.register(models.Room, RoomAdmin)
