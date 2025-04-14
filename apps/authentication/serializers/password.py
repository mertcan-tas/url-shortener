from core.serializers import BaseSerializer
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
import re

class ChangePasswordSerializer(BaseSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_password2 = serializers.CharField(required=True, write_only=True)
    
    def validate_old_password(self, old_password):
        user = self.context['request'].user
        if not check_password(old_password, user.password):
            raise serializers.ValidationError("Wrong password.")
        return old_password
    
    def validate_new_password(self, new_password):
        # Password complexity checks
        if len(new_password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        if not re.search(r'[A-Z]', new_password):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', new_password):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', new_password):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
            raise serializers.ValidationError("Password must contain at least one special character.")
        
        return new_password
    
    def validate(self, attrs):
        # Check if new passwords match
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password2": "Password fields didn't match."})
        
        # Check if new password is different from old password
        user = self.context['request'].user
        if check_password(attrs['new_password'], user.password):
            raise serializers.ValidationError({"new_password": "New password cannot be the same as the old password."})
        
        return attrs
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user