from django.contrib import admin
from .models import AccountModel, PatientModel, DoctorModel
# Register your models here.
admin.site.register(AccountModel) 
admin.site.register(PatientModel) 
admin.site.register(DoctorModel)  