from django.contrib import admin
from .models import Vessels_in_Port


# Register your models here.

class VesselAdmin(admin.ModelAdmin):
    list_display = ["vessel_name","terminal","run_date"]


admin.site.register(Vessels_in_Port,VesselAdmin)


