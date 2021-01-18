from django.contrib import admin
from lodge import models
from django.utils.safestring import mark_safe

from django.contrib import messages
from django.utils.translation import ngettext

from django.shortcuts import render
from django.http import HttpResponseRedirect


class LodgeImageAdmin(admin.StackedInline):
    model = models.LodgeImage
    extra = 1
    max_num = 3


class LodgeAdmin(admin.ModelAdmin):
    inlines = [LodgeImageAdmin]
    list_display = [
        'name', 'address', 'state', 'num_of_flats', 'details', 'owner'
    ]

    # readonly_fields = ["front_image"]

    # def front_image(self, obj):
    #     return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
    #         url=obj.image.url,
    #         width=obj.image.width,
    #         height=obj.image.height,
    #     )
    #     )


class RoomAdmin(admin.ModelAdmin):
    list_display = [
        'lodge', 'room_number', 'tenant', 'occupied', 'rent_start_date',
        'rent_end_date'
    ]
    list_filter = ('lodge', 'occupied', 'rent_start_date', 'rent_end_date')
    readonly_fields = ('transaction_id',)
    actions = ['evict_tenant']

    def evict_tenant(self, request, queryset):

        if 'apply' in request.POST:
            updated = queryset.update(tenant=None, occupied=False, room_mates=None, rent_start_date=None,
                                      rent_end_date=None, transaction_id=None, terms_agreed=False)
            self.message_user(request, ngettext(
                '%d room was successfully evicted.',
                '%d rooms were successfully evicted.',
                updated,
            ) % updated, messages.SUCCESS)
            return HttpResponseRedirect(request.get_full_path())
        elif 'cancel' in request.POST:
            return HttpResponseRedirect(request.get_full_path())

        return render(request,
                      'admin/evict_intermediate.html',
                      context={'rooms': queryset})

    evict_tenant.short_description = "Evict tenants from selected rooms"


admin.site.register(models.Lodge, LodgeAdmin)
admin.site.register(models.Room, RoomAdmin)
