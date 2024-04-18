from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from . import models
from . import serializers
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from .serializers import UserSerializer, profileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token as AuthToken

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.AccountModel.objects.all()
    serializer_class = serializers.UserSerializer




class UserLoginApiView(APIView):

    def get(self, request):
        return Response({'message': 'Welcome to the login page'})
    
    def post(self, request):
        serializer = serializers.LoginSerializer(data = self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username= username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                User_model = models.AccountModel.objects.get(account = user)
                user_type = User_model.user_role
                return Response({'token' : token.key, 'user_id' : user.id, 'user_role': user_type})
            else:
                return Response({'error' : "Invalid Credential"})
        return Response(serializer.errors)



class UserProfileViewSet(APIView):
    # permission_classes = [IsAuthenticated]
    # serializer_class = serializers.profileSerializer

    def get(self, request):
        
            token_key = request.headers.get('Authorization')
            if token_key:
                parts = token_key.split()
                if len(parts) == 2 and parts[0].lower() == 'bearer':
                    received_token = parts[1]
                auth_token_instance = AuthToken.objects.get(key=received_token)
                token = Token.objects.get(key=auth_token_instance)
                userModel_instance = models.AccountModel.objects.get(account = token.user)
                print(userModel_instance)
                serializer = profileSerializer(userModel_instance)
                return Response(serializer.data)
            

            # serializer = profileSerializer()
            return Response('your auth token not found')
    
    def post(self, request):
        serializer = profileSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(request)
            # username = serializer.validated_data['email']
            print("profile view username:", user)
        else:
            print("Validation errors:", serializer.errors)

        return Response({'status': 'success'})

    

class UserRegistrationApiView(APIView):
    serializer_class = serializers.RegistrationSerializer
    
    def get(self, request):
        return Response({'message': 'Welcome to the registration page'})
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save(request)


            token = default_token_generator.make_token(user)

            uid = urlsafe_base64_encode(force_bytes(user.pk))

            confirm_link = f"http://127.0.0.1:5000/user/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            # email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            email_body = f'uid: {uid} token: {token} {confirm_link}'
            
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Check your mail for confirmation")
        return Response(serializer.errors)


class UserLogoutView(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                auth_token = parts[1]
                # print(request.user.auth_token)
        logout(request)
        return redirect('login')
    


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')
    