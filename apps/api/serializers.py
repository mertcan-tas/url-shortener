from rest_framework import serializers
from core.serializers import BaseModelSerializer

from django.contrib.auth import get_user_model
from api.models import ShortURL

User = get_user_model()

class ShortURLSerializer(BaseModelSerializer):
    short_url = serializers.SerializerMethodField()
    real_time_visits = serializers.IntegerField(read_only=True, required=False)
    extra_kwargs = {
        'user': {'required': False}
    }    

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
        ]
        read_only_fields = [
            'short_code', 
            'created_at', 
            'visits', 
            'real_time_visits', 
            'user', 
        ]
    
    def get_short_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return f"{request.scheme}://{request.get_host()}/{obj.short_code}"
        return obj.short_code
