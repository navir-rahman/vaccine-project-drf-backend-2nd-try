from rest_framework import serializers
from .models import Vaccine, VaccineRecord
# from django.utils import timezone
from account.models import DoctorModel
from datetime import timedelta

class VaccineSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(many=False)
    class Meta:
        model = Vaccine
        fields = '__all__'

class addVaccineSerializer(serializers.ModelSerializer ):
    # initiated_by = serializers.StringRelatedField(many=False)
    class Meta:
        model = Vaccine
        fields = '__all__'

    def create(self, validated_data, user_instance=None):
        if user_instance is None:
            user_instance = self.context.get('user_instance')
            initiated_by = DoctorModel.objects.get(doctor = user_instance)
        print(user_instance)

        
        name = validated_data['name']
        image = validated_data['image']
        description = validated_data['description']
        dose_count = validated_data['dose_count']
        status = validated_data['status']
        campaign_name = validated_data['campaign_name']
        # initiated_date = timezone.now().strftime('%Y-%m-%d')
        first_dose_date = validated_data['first_dose_date']
        # second_dose_date = validated_data['first_dose_date']
        second_dose_date = first_dose_date + timedelta(days=3)
            
        vaccineInstance = Vaccine.objects.create(name = name, image = image, description = description, dose_count = dose_count, status = status, campaign_name = campaign_name, initiated_by = initiated_by, first_dose_date = first_dose_date, second_dose_date = second_dose_date) 
        print(vaccineInstance)
        return False
    
    # def update(self, instance, validated_data):
    #     # Update each field in the instance with the validated data
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.image = validated_data.get('image', instance.image)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.dose_count = validated_data.get('dose_count', instance.dose_count)
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.campaign_name = validated_data.get('campaign_name', instance.campaign_name)
    #     # You may need to handle initiated_date and initiated_by differently for updates
    #     # instance.initiated_date = timezone.now().strftime('%Y-%m-%d')
    #     instance.initiated_by = DoctorModel.objects.get(doctor=self.context.get('user_instance'))
        
    #     instance.save()
    #     return instance

class VaccineRecordSerializer(serializers.ModelSerializer):
    # vaccine = serializers.StringRelatedField(many=False)
    # patient = serializers.StringRelatedField(many=False)

    class Meta:
        model = VaccineRecord
        fields = '__all__'
    


