from django.contrib import admin
from .models import Vaccine, VaccineRecord
# Register your models here.
admin.site.register(Vaccine)
admin.site.register(VaccineRecord)