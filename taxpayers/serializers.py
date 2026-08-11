from rest_framework import serializers
from .models import TaxpayerMaster, MultipleLicenseReference


class TaxpayerMasterSerializer(serializers.ModelSerializer):
    """Serializer for Taxpayer Master model"""
    class Meta:
        model = TaxpayerMaster
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class MultipleLicenseReferenceSerializer(serializers.ModelSerializer):
    """Serializer for Multiple License Reference model"""
    class Meta:
        model = MultipleLicenseReference
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']