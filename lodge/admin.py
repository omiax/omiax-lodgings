from django.contrib import admin
from lodge import models
from django.utils.safestring import mark_safe


class LodgeAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'address', 'state', 'num_of_rooms', 'details', 'owner'
    ]
    readonly_fields = ["front_image"]

    def front_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.url,
            width=obj.image.width,
            height=obj.image.height,
        )
        )


class RoomAdmin(admin.ModelAdmin):
    list_display = [
        'lodge', 'room_number', 'tenant', 'occupied', 'rent_start_date',
        'rent_end_date'
    ]
    readonly_fields = ('transaction_id',)


admin.site.register(models.Lodge, LodgeAdmin)
admin.site.register(models.Room, RoomAdmin)
