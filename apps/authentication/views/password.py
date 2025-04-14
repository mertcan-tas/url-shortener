from rest_framework import generics, status, permissions
from rest_framework.response import Response
from authentication.serializers import ChangePasswordSerializer
from decouple import config

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            

            
            return Response({"message": "Password successfully changed!"}, 
                          status=status.HTTP_200_OK)
                          
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)