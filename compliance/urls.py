from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComplianceMonitoringViewSet, ComplianceRiskReferralViewSet, EnforcementRecoveryViewSet, run_risk_assessment, period_risk_assessment_view, compliance_risk_dashboard

router = DefaultRouter()
router.register(r'compliance-monitoring', ComplianceMonitoringViewSet, basename='compliance-monitoring')
router.register(r'compliance-risk-referral', ComplianceRiskReferralViewSet, basename='compliance-risk-referral')
router.register(r'enforcement-recovery', EnforcementRecoveryViewSet, basename='enforcement-recovery')

urlpatterns = [
    path('compliance_risk_dashboard/', compliance_risk_dashboard, name='compliance_risk_dashboard'),
    path('run_risk_assessment/', run_risk_assessment, name='run_risk_assessment'),
    path('period_risk_assessment/', period_risk_assessment_view, name='period_risk_assessment'),
    path('', include(router.urls)),
]