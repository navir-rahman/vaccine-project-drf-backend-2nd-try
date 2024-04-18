from django.db import models
from django.contrib.auth.models import User
# from Campaign.models import Campaign

user_roles = (
    ('doctor', 'Doctor'),
    ('patient', 'Patient'),
)

class AccountModel(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_model')
    date_of_birth = models.DateField()
    nid = models.IntegerField()
    # past_medical_reports = models.TextField()
    user_role = models.CharField(max_length=20, choices=user_roles)


    def __str__(self):
        return self.account.username


class PatientModel(models.Model):
    patient = models.OneToOneField(AccountModel, on_delete=models.CASCADE, related_name='patient')
    past_medical_reports = models.TextField()

    def __str__(self):
        return self.patient.account.username

    

class DoctorModel(models.Model):
    doctor = models.OneToOneField(AccountModel, on_delete=models.CASCADE, related_name='user')
    # vaccines = models.ManyToManyField(Vaccine,  related_name='vaccines', default= None, blank=True)
    # campaign = models.ManyToManyField(Campaign,  related_name='campaign')
    

    def __str__(self):
        return self.doctor.account.username

    