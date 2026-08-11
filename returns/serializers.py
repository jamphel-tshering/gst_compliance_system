from rest_framework import serializers
from .models import GSTReturn


class GSTReturnSerializer(serializers.ModelSerializer):
    """Serializer for GST Return model"""
    class Meta:
        model = GSTReturn
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']