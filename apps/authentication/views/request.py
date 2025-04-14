from rest_framework import status
from rest_framework.permissions import AllowAny 
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from authentication.tasks import send_password_reset_email

User = get_user_model()

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"
                full_name = user.full_name
                # Send password reset email asynchronously
                send_password_reset_email.delay(email, reset_url, full_name)
                
                return Response({"message": "Password reset email has been sent."}, 
                              status=status.HTTP_200_OK)
            return Response({"message": "User with this email does not exist."}, 
                          status=status.HTTP_404_NOT_FOUND)
        return Response({"email": ["This field is required."]}, 
                       status=status.HTTP_400_BAD_REQUEST)