from django.forms import NullBooleanField
from django.shortcuts import render
from rest_framework.fields import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions, generics, mixins, status, viewsets
from common.serializers import UserSerializer
from core.models import User


# Create your views here.
class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data

        if 'password' not in data or 'confirm_password' not in data:
            return Response({"message": "Both password and password confirmation are required"}, status=status.HTTP_400_BAD_REQUEST)

        if data['password'] != data['confirm_password']:
            return Response({"message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        
        data['is_ambassador'] = 0
        
        serializer = UserSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class LoginAPIView(APIView):
    def post(self, request):
        data = request.data
        
        if "email" in data:
            try:
                user = User.objects.get(email=data['email'].lower())
            except ObjectDoesNotExist:
                return Response({"message": "Invalid email!"}, status=status.HTTP_400_BAD_REQUEST)
        elif "username" in data:
            try:
                user = User.objects.get(username=data['username'].lower())
            except ObjectDoesNotExist:
                return Response({"message": "Invalid username!"}, status=status.HTTP_400_BAD_REQUEST)
            
        if not user.check_password(data["password"]):
            return Response({"message": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(UserSerializer(user).data)
 