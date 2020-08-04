from django.contrib import admin
from django.contrib.admin import TabularInline, ModelAdmin

from hotel import models


admin.site.register(models.City)
# admin.site.register(models.Hotel)
# admin.site.register(models.Facility)
# admin.site.register(models.Room)


class FacilityInline(TabularInline):
    model = models.Facility
    extra = 1


class BreadcrumbInline(TabularInline):
    model = models.Breadcrumb
    extra = 1


class RoomInline(TabularInline):
    model = models.Room
    extra = 1


@admin.register(models.Hotel)
class HotelAdmin(ModelAdmin):
    inlines = [
        FacilityInline,
        BreadcrumbInline,
        RoomInline,
    ]
