from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, AuditLog, SystemSettings
from django.shortcuts import render
from django.urls import reverse
from django.contrib.admin import AdminSite


# Main Dashboard View
def main_dashboard(request):
    """Main dashboard with links to all module dashboards"""
    dashboard_links = [
        {
            'title': 'Taxpayer Management',
            'url': '/admin/taxpayers/taxpayermaster/',
            'description': 'Manage taxpayer registration and profiles',
            'icon': '👥'
        },
        {
            'title': 'GST Returns',
            'url': '/admin/returns/gstreturn/',
            'description': 'Process and monitor GST returns',
            'icon': '📋'
        },
        {
            'title': 'Compliance Monitoring',
            'url': '/admin/compliance/compliancemonitoring/',
            'description': 'Compliance monitoring, risk assessment, and enforcement',
            'icon': '✅'
        },
        {
            'title': 'Audit & Refund',
            'url': '/admin/audit_refund/auditcase/',
            'description': 'Audit case management and refund processing',
            'icon': '🔍'
        },
        {
            'title': 'Reporting',
            'url': '/admin/reporting/reporttemplate/',
            'description': 'Centralized Reporting and Analytics Layer',
            'icon': '📊'
        },
    ]
    
    context = {
        'title': 'RRCO/GST Mongar Administration',
        'subtitle': 'Main Dashboard',
        'dashboard_links': dashboard_links,
    }
    
    return render(request, 'core/main_dashboard.html', context)


# Use default admin site for core to avoid circular import
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'get_role_display', 'is_active', 'created_at']
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
