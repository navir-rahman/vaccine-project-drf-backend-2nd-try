from django.db import models
from account.models import DoctorModel, PatientModel
# from django.utils import timezone

class Vaccine(models.Model):
    status_choices = (
        ('active', 'active'),
        ('complete', 'complete'),
        ('continuous', 'continuous'),
    )
    
    name = models.CharField(max_length=100)
    image = models.ImageField(default=None, blank=True, null=True, upload_to='vaccine/images/')
    description = models.TextField()
    dose_count = models.IntegerField(default=3, null=True, blank=True)
    initiated_by = models.ForeignKey(DoctorModel, on_delete=models.CASCADE, default = False, null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    campaign_name = models.CharField(max_length=20, default='null', blank=True, null = True)
    
    first_dose_date = models.DateField(null = True, blank=True )
    second_dose_date = models.DateField(null = True, blank=True )

    # initiated_date = models.DateTimeField(default=timezone.now().strftime('%Y-%m-%d'), null = True, blank=True )

    def __str__(self):
        return self.name


class VaccineRecord(models.Model):
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name='vaccine_name')
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE, related_name='patient_name')
    date_taken = models.DateField()

    def __str__(self):
        return self.vaccine