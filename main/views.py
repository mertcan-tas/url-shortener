from django.shortcuts import render
from rest_framework.generics import (ListAPIView,RetrieveAPIView,DestroyAPIView,RetrieveUpdateAPIView,CreateAPIView, UpdateAPIView)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseRedirect
from main.permissions import IsOwner

from rest_framework.permissions import IsAuthenticated
from main.models import ShortenedLink
from main.permissions import IsOwner
from main.serializers import ShortenedLinkSerializer

class ShortenedLinkCreateAPIView(CreateAPIView):
    queryset = ShortenedLink.objects.all()
    serializer_class = ShortenedLinkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class ShortenedLinkGetAPIView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            link = ShortenedLink.objects.get(id=id)
        except ShortenedLink.DoesNotExist:
            return Response({"error": "Shortened link not found."}, status=status.HTTP_404_NOT_FOUND)
    
        link.increment_click_count()
        return HttpResponseRedirect(link.url)

class ShortenedLinkDeleteAPIView(DestroyAPIView):
    queryset = ShortenedLink.objects.all()
    serializer_class = ShortenedLinkSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'id' 

class ShortenedLinkUserListAPIView(ListAPIView):
    serializer_class = ShortenedLinkSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = ShortenedLink.objects.filter(user=self.request.user).order_by('-created_at')
        return queryset

class ShortenedLinkUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = ShortenedLinkSerializer
    queryset = ShortenedLink.objects.all()

    def get_object(self):
        user = self.request.user
        contact = ShortenedLink.objects.get(user=user)
        return contact

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
