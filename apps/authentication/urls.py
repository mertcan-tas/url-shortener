from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import (
    RegisterView, LoginView, ChangePasswordView,
    PasswordResetRequestView, PasswordResetConfirmView, CurrentUserView
)

urlpatterns = [
    path('user/', CurrentUserView.as_view(), name='user'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]