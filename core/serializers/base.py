from rest_framework import serializers

class BaseSerializer(serializers.Serializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key, value in data.items():
            if value is None:
                data[key] = '—'
        return data

class BaseModelSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data

    def validate(self, attrs):
        return super().validate(attrs)