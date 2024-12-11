from rest_framework import serializers
from django.core.validators import URLValidator
from main.models import ShortenedLink

class ShortenedLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedLink
        fields = ['id','url']
        read_only_fields = ['id', 'created_at', 'updated_at', 'click_count']
    
    def validate_url(self, value):
        validator = URLValidator()
        try:
            validator(value)
        except:
            raise serializers.ValidationError("Geçerli bir URL girin.")
        return value
    