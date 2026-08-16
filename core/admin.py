from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, AuditLog, SystemSettings
from django.shortcuts import render
from django.urls import reverse
from django.contrib.admin import AdminSite


# Main Dashboard View
def main_dashboard(request):
    """Main dashboard with live statistics and dashboards for all modules"""
    from taxpayers.models import TaxpayerMaster
    from returns.models import GSTReturn
    from compliance.models import ComplianceMonitoring, ComplianceRiskReferral
    from audit_refund.models import AuditCase, RefundRegister
    
    # Taxpayer Statistics
    total_taxpayers = TaxpayerMaster.objects.filter(is_primary_license=True).count()
    active_taxpayers = TaxpayerMaster.objects.filter(status='Active', is_primary_license=True).count()
    inactive_taxpayers = TaxpayerMaster.objects.filter(status='Inactive', is_primary_license=True).count()
    
    # GST Returns Statistics
    total_returns = GSTReturn.objects.count()
    filed_returns = GSTReturn.objects.filter(filing_status='Filed').count()
    pending_returns = GSTReturn.objects.filter(filing_status='Pending').count()
    overdue_returns = GSTReturn.objects.filter(filing_status='Overdue / Non-Filer').count()
    
    # Compliance Statistics
    total_compliance = ComplianceMonitoring.objects.count()
    compliant_count = ComplianceMonitoring.objects.filter(compliance_status='Compliant').count()
    non_compliant_count = ComplianceMonitoring.objects.filter(compliance_status__in=['Non-Filer', 'Late Filer', 'Payment Default']).count()
    
    # Risk Assessment Statistics
    total_risk = ComplianceRiskReferral.objects.count()
    high_risk = ComplianceRiskReferral.objects.filter(risk_level='High').count()
    medium_risk = ComplianceRiskReferral.objects.filter(risk_level='Medium').count()
    low_risk = ComplianceRiskReferral.objects.filter(risk_level='Low').count()
    
    # Audit Statistics
    total_audits = AuditCase.objects.count()
    open_audits = AuditCase.objects.filter(status='Open').count()
    completed_audits = AuditCase.objects.filter(status='Completed').count()
    
    # Refund Statistics
    total_refunds = RefundRegister.objects.count()
    pending_refunds = RefundRegister.objects.filter(status='Pending').count()
    approved_refunds = RefundRegister.objects.filter(status='Approved').count()
    
    dashboard_stats = {
        'taxpayers': {
            'total': total_taxpayers,
            'active': active_taxpayers,
            'inactive': inactive_taxpayers,
            'url': '/admin/taxpayers/taxpayermaster/',
            'icon': '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#1a237e" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>'
        },
        'returns': {
            'total': total_returns,
            'filed': filed_returns,
            'pending': pending_returns,
            'overdue': overdue_returns,
            'url': '/admin/returns/gstreturn/',
            'icon': '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#1a237e" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>'
        },
        'compliance': {
            'total': total_compliance,
            'compliant': compliant_count,
            'non_compliant': non_compliant_count,
            'url': '/admin/compliance/compliancemonitoring/',
            'icon': '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#1a237e" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>'
        },
        'risk': {
            'total': total_risk,
            'high': high_risk,
            'medium': medium_risk,
            'low': low_risk,
            'url': '/compliance/compliance_risk_dashboard/',
            'icon': '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#1a237e" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>'
        },
        'audit': {
            'total': total_audits,
            'open': open_audits,
            'completed': completed_audits,
            'url': '/admin/audit_refund/auditcase/',
            'icon': '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#1a237e" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>'
        },
        'refund': {
            'total': total_refunds,
            'pending': pending_refunds,
            'approved': approved_refunds,
            'url': '/admin/audit_refund/refundregister/',
            'icon': '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#1a237e" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect><line x1="1" y1="10" x2="23" y2="10"></line></svg>'
        },
    }
    
    context = {
        'title': 'RRCO/GST Mongar Administration',
        'subtitle': 'Main Dashboard',
        'dashboard_stats': dashboard_stats,
    }
    
    return render(request, 'core/main_dashboard.html', context)


# Use default admin site for core to avoid circular import
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['get_full_name', 'email', 'username', 'get_role_display', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    # Allow all users to view and add users for basic functionality
    def has_add_permission(self, request):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'timestamp', 'ip_address']
    list_filter = ['action', 'timestamp']
    search_fields = ['user__email', 'description']
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 'description', 'ip_address', 'timestamp']
    ordering = ['-timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ['system_name', 'organization_name', 'contact_email', 'updated_at', 'updated_by']
    search_fields = ['system_name', 'organization_name', 'contact_email']
    readonly_fields = ['updated_at', 'updated_by']
    
    def has_add_permission(self, request):
        # Only allow one system settings record
        if SystemSettings.objects.exists():
            return False
        return request.user.is_superuser or request.user.is_administrator()
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_administrator()
