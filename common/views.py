from django.db import IntegrityError
from django.forms import NullBooleanField
from django.shortcuts import render
from rest_framework.fields import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions, generics, mixins, status, viewsets
from common.authentication import JWTAuthentication
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
        
        
        token = JWTAuthentication.generate_jwt(user.id)
        response = Response()
        response.set_cookie(key="user_session", value=token, httponly=True)
        response.data = {
            "message": "Successfully logged in!"
        }
        
        return response

class UserAPIView(APIView):
    # User needed to be login
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response(UserSerializer(request.user).data)
    
class LogoutAPIView(APIView):
    # User needed to be login
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, _):
        response = Response()
        response.delete_cookie(key="user_session")
        response.data = {
            "message": "Success"
        }
        return response
    
class ProfileInfoAPIView(APIView):
    # User needed to be login
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]    
    
    def put(self, request, pk=None):
        try:
            user = request.user
            serializer = UserSerializer(user, data=request.data, context={'request': request}, partial=True)  # Allow partial updates
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
            
        except exceptions.ValidationError as e:
            # Generate a more user-friendly message that includes the field name
            errors = {key: value[0] for key, value in e.detail.items()}
            first_field = next(iter(errors))
            field_name = first_field.replace('_', ' ').capitalize()
            if 'already exists' in errors[first_field]:
                message = f"{field_name.capitalize()} already exists."
            else:
                message = f"{field_name} error: {errors[first_field]}"
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        
class ProfilePasswordAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk=None):
        try:
            user = request.user
            data = request.data
            
            if data["password"] != data["confirm_password"]:
                return Response({"message": "Password do not match!"})
            
            user.set_password(data["password"])
            user.save()
            return Response(UserSerializer(user).data)
        except Exception:
            return Response({'message': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)