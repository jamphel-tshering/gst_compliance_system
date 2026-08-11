from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import AuditRegister, ComplianceRiskRegister, AuditAllotment
from .serializers import AuditRegisterSerializer, ComplianceRiskRegisterSerializer, AuditAllotmentSerializer


class AuditRegisterViewSet(viewsets.ModelViewSet):
    """ViewSet for Audit Register model"""
    queryset = AuditRegister.objects.all()
    serializer_class = AuditRegisterSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gstin', 'tax_period', 'assessment_type', 'status']
    search_fields = ['gstin', 'taxpayer_name', 'asc_no']
    ordering_fields = ['assessment_date', 'taxpayer_name']
    ordering = ['-assessment_date']
    
    @action(detail=False, methods=['get'])
    def open_audits(self, request):
        """Get only open audits"""
        open_audits = self.queryset.filter(status__in=['pending', 'in_progress'])
        serializer = self.get_serializer(open_audits, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Get audits grouped by status"""
        status_data = {}
        for status in ['pending', 'in_progress', 'completed', 'closed']:
            status_data[status] = self.queryset.filter(status=status).count()
        return Response(status_data)


class ComplianceRiskRegisterViewSet(viewsets.ModelViewSet):
    """ViewSet for Compliance Risk Register model"""
    queryset = ComplianceRiskRegister.objects.all()
    serializer_class = ComplianceRiskRegisterSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['assessment_period', 'overall_risk_level', 'audit_selection', 'assessment_status']
    search_fields = ['risk_id', 'taxpayer__taxpayer_name', 'taxpayer__gstin']
    ordering_fields = ['overall_risk_score', 'assessment_period', 'taxpayer__taxpayer_name']
    ordering = ['-overall_risk_score']
    
    @action(detail=False, methods=['get'])
    def high_risk(self, request):
        """Get only high-risk cases"""
        high_risk = self.queryset.filter(overall_risk_level__in=['critical', 'high'])
        serializer = self.get_serializer(high_risk, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def selected_for_audit(self, request):
        """Get taxpayers selected for audit"""
        selected = self.queryset.filter(audit_selection='selected')
        serializer = self.get_serializer(selected, many=True)
        return Response(serializer.data)


class AuditAllotmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Audit Allotment model"""
    queryset = AuditAllotment.objects.all()
    serializer_class = AuditAllotmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tax_period', 'dzongkhag', 'assessor', 'allotment_date']
    search_fields = ['gstin', 'taxpayer_name', 'assessor__username']
    ordering_fields = ['allotment_date', 'taxpayer_name']
    ordering = ['-allotment_date']