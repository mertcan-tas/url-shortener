from django.urls import path

from account.views import  RegisterEmailView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('register/', RegisterEmailView.as_view(), name='register'),
]