from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuditRegisterViewSet, ComplianceRiskRegisterViewSet, AuditAllotmentViewSet

router = DefaultRouter()
router.register(r'audit-register', AuditRegisterViewSet, basename='audit-register')
router.register(r'compliance-risk', ComplianceRiskRegisterViewSet, basename='compliance-risk')
router.register(r'audit-allotment', AuditAllotmentViewSet, basename='audit-allotment')

urlpatterns = [
    path('', include(router.urls)),
]