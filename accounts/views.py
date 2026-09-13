from django.shortcuts import render , get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response 
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import serializers ,SignUpSerializer , UserSerializer
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta ,timezone
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

# Create your views here.

@api_view(['POST'])
def register(request):
    data = request.data
    user = SignUpSerializer(data = data)

    if user.is_valid():
        if not User.objects.filter(username= data['email']).exists():
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                username = data['email'],
                password = make_password(data['password']),

            )
            return Response({'details':'Your account registered succesfully!'},status=status.HTTP_201_CREATED)
        else:
            return Response({'error':'This email already exist!'},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user.errors)
@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def current_user(request):
    user  = UserSerializer(request.user, many= False)
    return Response(user.data)



@api_view(['PUT']) 
@permission_classes([IsAuthenticated])
def update_user(request):
    logged_user  = request.user
    incoming_data = request.data

    logged_user.first_name = incoming_data.get('first_name',logged_user.first_name)
    logged_user.last_name = incoming_data.get('last_name', logged_user.last_name)
    logged_user.username = incoming_data.get('email', logged_user.username)
    logged_user.email = incoming_data.get('email', logged_user.email)
    
    if incoming_data.get('password'):
        logged_user.password = make_password(incoming_data['password'])

    logged_user.save()
    serializer = UserSerializer(logged_user, many=False)
    return Response(serializer.data)


def get_current_host(request):
    protocol = request.is_secure( ) and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol = protocol , host = host)



   
@api_view(['POST'])
def forget_password(request):
    incoming_data = request.data
    user = get_object_or_404(User,email =incoming_data['email'])
    token = get_random_string(40)
    expired_date = timezone.now() + timedelta(minutes=10)
    user.profile.reset_password_token =token
    user.profile.reset_password_expire_token = expired_date
    user.profile.save()
    host = get_current_host(request)
    protocol = request.is_secure() and 'https' or 'http'
    link = f"{protocol}://{host}/{token}/".format(protocol = protocol , host = host)
    body = f"Your password reset link is :{link}"
    send_mail(
    "Password reset from eMerket",
    body,
    settings.DEFAULT_FROM_EMAIL,   
    [incoming_data['email']],       
    fail_silently=False,
    )
    return Response({"details": 'password reset sent  to {email}'.format(email = incoming_data.get('email'))})

@api_view(['POST'])
def reset_password(request,token):
    incoming_data = request.data
    user = get_object_or_404(User,profile__reset_password_token = token)

    if user.profile.reset_password_expire.replace(tzinfo = None) < datetime.now():
        return Response({"error":"token is expired"}, status=status.HTTP_400_BAD_REQUEST)


    if incoming_data.get('password') != incoming_data.get('confirmPassword'):
        return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

    user.password =make_password(incoming_data.get('password'))
    user.profile.reset_password_token =token
    user.profile.reset_password_expire_token = expired_date

   
    expired_date = timezone.now() + timedelta(minutes=10)
    user.profile.reset_password_token =token
    user.profile.reset_password_expire_token = expired_date
    user.profile.save()
    user.save()
    return Response({"details": 'password reset is done '})



