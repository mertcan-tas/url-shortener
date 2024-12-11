from django.urls import path

from main.views import (ShortenedLinkCreateAPIView,
                        ShortenedLinkGetAPIView,
                        ShortenedLinkDeleteAPIView,
                        ShortenedLinkUserListAPIView,
                        ShortenedLinkUpdateAPIView
                        )

urlpatterns = [
    path('get/<str:id>/', ShortenedLinkGetAPIView.as_view(), name='redirect-shortened-link'),
    
    path('create/', ShortenedLinkCreateAPIView.as_view(), name='create-shortened-link'),
    path('user/', ShortenedLinkUserListAPIView.as_view(), name='user-shortened-links'),
    path('<str:id>/delete/', ShortenedLinkDeleteAPIView.as_view(), name='delete-shortened-link'),
    path('<str:id>/update/', ShortenedLinkUpdateAPIView.as_view(), name='update-shortened-link'),
]

