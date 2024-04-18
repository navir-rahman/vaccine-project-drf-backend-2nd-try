from rest_framework import serializers
from .models import AccountModel, PatientModel, DoctorModel
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

user_roles = (
    (1, 'doctor'),
    (2, 'patient'),
)


class UserSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = AccountModel 
        fields = '__all__'


        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)


class Usersereal(serializers.ModelSerializer):
    username = serializers.CharField(required = False)
    first_name = serializers.CharField(required = False)
    last_name = serializers.CharField(required = False)
    email = serializers.CharField(required = False)
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'last_name']
    
    def save(self, request, *args, **kwargs):
        
        username = self.validated_data['username']
        user = User.objects.get(username=username)

        user.first_name = self.validated_data['first_name']
        user.last_name = self.validated_data['last_name']
        user.email = self.validated_data['email']

        user.save()

        return user
    

class profileSerializer(serializers.ModelSerializer):
    # past_medical_reports = serializers.CharField(required = True)
    nid = serializers.CharField()
    user_role = serializers.CharField()
    date_of_birth = serializers.DateField()

    account = Usersereal(many=False, required = False)
    class Meta:
        model = AccountModel
        fields = [ 'nid', 'user_role',  'date_of_birth', 'account']  
    
    def save(self,request, *args, **kwargs):
        serializer = Usersereal(data=request.data)
        if serializer.is_valid():
            user = serializer.save(request)

            AccountModelInstance = AccountModel.objects.get(account=user)
            
            AccountModelInstance.nid = self.validated_data['nid']
            AccountModelInstance.date_of_birth = self.validated_data['date_of_birth']

            AccountModelInstance.save()
            print('profile serializer', AccountModelInstance)

        return user
    
    
        

        
# class profileSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(required = True)
#     email = serializers.CharField(required = True)
#     first_name = serializers.CharField(required = True)
#     last_name = serializers.CharField(required = True)
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'first_name', 'last_name']
    
#     def save(self,request, *args, **kwargs):
#         username = self.validated_data['username']
#         user = User.objects.get(username=username)
        
#         # Update user attributes
#         user.first_name = self.validated_data['first_name']
#         user.last_name = self.validated_data['last_name']
#         user.email = self.validated_data['email']
        
#         print(user)
#         # Save changes
#         user.save()

#         return user

class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required = True)
    first_name = serializers.CharField(required = True)
    last_name = serializers.CharField(required = True)
    email = serializers.CharField(required = True)
    password = serializers.CharField(required = True)
    confirm_password = serializers.CharField(required=True)
    past_medical_reports = serializers.CharField(required = True)
 
    class Meta:
        model = AccountModel
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'nid', 'user_role', 'past_medical_reports', 'date_of_birth']
    
    def save(self, request, *args, **kwargs):
        print(self.validated_data)
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        nid = self.validated_data.get('nid')
        user_role = self.validated_data.get('user_role')
        past_medical_reports = self.validated_data.get('past_medical_reports')
        date_of_birth = self.validated_data.get('date_of_birth')
        
        if password != password2:
            raise serializers.ValidationError({'error': "Passwords don't match"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email already exists"})
        
        # user = AccountModel(username=username, email=email, first_name=first_name, last_name=last_name, nid=nid, user_role=user_role, past_medical_reports=past_medical_reports, date_of_birth=date_of_birth)
        user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.is_active = True
        user.save()
        user_instance = AccountModel.objects.create(account=user, nid=nid, user_role=user_role, date_of_birth=date_of_birth)
        user_instance.save()
        auth_user = authenticate(request=request, username=request.data['username'], password=request.data['password'])
        if auth_user is not None:
            login(request, auth_user)

        if user_role == 'patient':
            PatientModel.objects.create(patient=user_instance,past_medical_reports=past_medical_reports)
        else:
            DoctorModel.objects.create(doctor=user_instance)
        return user
