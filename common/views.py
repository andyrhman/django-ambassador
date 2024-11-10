from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions, generics, mixins, status, viewsets
from common.serializers import UserSerializer


# Create your views here.
class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data

        if 'password' not in data or 'password_confirm' not in data:
            return Response({"message": "Both password and password confirmation are required"}, status=status.HTTP_400_BAD_REQUEST)

        if data['password'] != data['password_confirm']:
            return Response({"message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)