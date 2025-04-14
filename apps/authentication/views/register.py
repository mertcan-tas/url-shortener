from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from authentication.serializers import RegisterSerializer
from decouple import config


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    def perform_create(self, serializer):
        user = serializer.save()