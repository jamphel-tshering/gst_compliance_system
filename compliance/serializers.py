from rest_framework import serializers
from .models import ComplianceMonitoring, ComplianceRiskReferral, EnforcementRecovery


class ComplianceMonitoringSerializer(serializers.ModelSerializer):
    """Serializer for Compliance Monitoring model"""
    class Meta:
        model = ComplianceMonitoring
        fields = '__all__'


class ComplianceRiskReferralSerializer(serializers.ModelSerializer):
    """Serializer for Compliance Risk & Referral model"""
    class Meta:
        model = ComplianceRiskReferral
        fields = '__all__'


class EnforcementRecoverySerializer(serializers.ModelSerializer):
    """Serializer for Enforcement & Recovery model"""
    class Meta:
        model = EnforcementRecovery
        fields = '__all__'