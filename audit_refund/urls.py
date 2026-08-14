from django.urls import path
from . import views
from .admin import audit_refund_dashboard

app_name = 'audit_refund'

urlpatterns = [
    path('', audit_refund_dashboard, name='admin_dashboard'),
    path('audit/', views.audit_dashboard, name='audit_dashboard'),
    path('audit/<int:audit_case_id>/', views.audit_case_detail, name='audit_case_detail'),
    path('refund/', views.refund_dashboard, name='refund_dashboard'),
    path('auto-create-audit-cases/', views.auto_create_audit_cases, name='auto_create_audit_cases'),
]