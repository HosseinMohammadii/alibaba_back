from django.contrib import admin
from hotel import models


admin.site.register(models.City)
admin.site.register(models.Hotel)
admin.site.register(models.Facility)
admin.site.register(models.Room)
