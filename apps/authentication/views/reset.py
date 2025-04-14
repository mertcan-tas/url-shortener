from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import PasswordResetConfirmSerializer

User = get_user_model()

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            # Initialize serializer with user context for validation
            serializer = PasswordResetConfirmSerializer(
                data=request.data,
                context={'user': user}
            )
            
            if serializer.is_valid():
                # Set the new password
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response(
                    {"message": "Password has been reset successfully."}, 
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {"message": "Invalid reset link or token expired."}, 
            status=status.HTTP_400_BAD_REQUEST
        )