from rest_framework import serializers
from .models import AuditRegister, ComplianceRiskRegister, AuditAllotment


class AuditRegisterSerializer(serializers.ModelSerializer):
    """Serializer for Audit Register model"""
    class Meta:
        model = AuditRegister
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ComplianceRiskRegisterSerializer(serializers.ModelSerializer):
    """Serializer for Compliance Risk Register model"""
    class Meta:
        model = ComplianceRiskRegister
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class AuditAllotmentSerializer(serializers.ModelSerializer):
    """Serializer for Audit Allotment model"""
    class Meta:
        model = AuditAllotment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']