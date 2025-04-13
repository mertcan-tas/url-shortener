from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ShortURL

User = get_user_model()

class ShortURLSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()
    real_time_visits = serializers.IntegerField(read_only=True, required=False)
    user_username = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = ShortURL
        fields = [
            'id', 
            'original_url', 
            'short_code', 
            'short_url', 
            'created_at', 
            'visits', 
            'real_time_visits', 
            'user', 
            'user_username'
        ]
        read_only_fields = [
            'short_code', 
            'created_at', 
            'visits', 
            'real_time_visits', 
            'user', 
            'user_username'
        ]
    
    def get_short_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return f"{request.scheme}://{request.get_host()}/{obj.short_code}"
        return obj.short_code
    
    def get_user_username(self, obj):
        if obj.user:
            return obj.user.username
        return None